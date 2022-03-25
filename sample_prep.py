import hashlib as hl
import math
from functools import lru_cache
from pathlib import Path

import click
import librosa as lr
import numpy as np
import soundfile as sf
from librosa.effects import split


def mono(sound):
    @lru_cache()
    def cache(idd):
        return sound[:, 0] + sound[:, 1]

    return cache(id(sound))


def norm(sound):
    @lru_cache()
    def cache(idd):
        peak = np.max(sound)
        return sound / peak

    return cache(id(sound))


def mono_norm(sound):
    @lru_cache()
    def cache(idd):
        s = mono(sound)
        return norm(s)

    return cache(id(sound))


def find_slice(sound, db, level=11):
    sound = mono_norm(sound)
    x = split(sound, top_db=db, frame_length=2**level, hop_length=2 ** (level - 2))
    return slice(x[0][0], x[-1][1])


def write(name, input, output, sound, sr):
    file_ = Path(output, f"{name}.wav")
    sf.write(file_, sound, sr, "PCM_16")
    hash = hl.md5()
    with file_.open("rb") as f:
        hash.update(f.read())
    dg = hash.hexdigest()[:8]
    output = Path(output, f"{name}_{dg}.wav")
    file_.rename(output)
    print(f"{input} -> {output}")


def cat(*args, **kwargs):
    return np.concatenate(*args, **kwargs)


def xmult(a, b):
    ll = len(b)
    first = a[:ll]
    second = a[ll:]
    first = first * b
    return cat((first, second))


@lru_cache()
def fadeshape(n):
    f = np.linspace(0, 1, n)
    return np.transpose([f, f])


def fade(sound):
    ll = len(sound) / 1
    att = fadeshape(min(400, ll))
    dec = fadeshape(min(1000, ll))
    sound = xmult(sound[::-1], dec)
    return xmult(sound[::-1], att)


def level(sound):
    sound = mono_norm(sound)
    return abs(10 * math.log10((np.sum(np.abs(sound)) / len(sound))))


def remove(sound, slc):
    first = sound[: slc.start]
    rest = sound[slc.stop :]
    return cat((first, rest))


def prep(input, output, i=""):
    sound, sr = sf.read(input)
    # input has to be 96k stereo
    assert sr == 96000
    assert len(sound[0]) == 2
    sound = sound[sr:-sr]
    sound = norm(sound)
    # write(f"{i}o", input, output, sound, sr)

    # Noise level heuristic
    slc = find_slice(sound, db=22, level=11)
    rem = remove(sound, slc)
    lev = min(10, level(rem) / 3)
    print_lev = int(lev * 10)
    i = f"{i}_{print_lev:02d}"

    # Remove most silence
    slc = find_slice(sound, db=20 + lev, level=11)
    sound = sound[slc]
    sound = norm(sound)

    # Finetune begining
    slc = find_slice(sound, db=18, level=8)
    start = max(0, slc.start - 128)
    sound = sound[start:]

    # Normalize and fade
    sound = norm(sound)
    sound = fade(sound)

    # Write normal
    write(i, input, output, sound, sr)

    # Write mono
    # write(f"{i}_mono", input, output, mono_norm(sound), sr)

    # Write low
    write(f"{i}_low", input, output, sound, 22050)

    # Resample for high
    sound = np.transpose(sound)
    sound = lr.resample(sound, orig_sr=sr, target_sr=sr / 4)
    sound = np.transpose(sound)
    sound = norm(sound)

    # Write high
    write(f"{i}_high", input, output, sound, sr)
    print("done")


def directory(path):
    path = Path(path)
    input = Path(path, "in")
    output = Path(path, "out")
    output.mkdir(exist_ok=True)
    i = 0
    for file_ in input.iterdir():
        if file_.is_file() and not file_.name.startswith("."):
            prep(file_, output, f"{i:03d}")
            i += 1


@click.command()
@click.argument(
    "path",
    type=click.Path(
        exists=True,
        dir_okay=True,
        writable=True,
        readable=True,
    ),
)
def cli(path):
    """Remove silence from percussive samples, normalize and write norm/high/low versions."""
    directory(path)


if __name__ == "__main__":
    cli()
