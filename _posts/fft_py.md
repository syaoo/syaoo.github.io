---
title: fft_py
tag: ['tag1','tag2']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---

abstract

<!--more-->Implementation

```

The DFT functionality in SciPy lives in the `scipy.fftpack` module. Among other things, it provides the following DFT-related functionality:

- `fft`, `fft2`, `fftn`

  Compute the DFT using the FFT algorithm in 1, 2, or `n` dimensions.

- `ifft`, `ifft2`, `ifftn`

  Compute the inverse of the DFT.

- `dct`, `idct`, `dst`, `idst`

  Compute the cosine and sine transforms, and their inverses.

- `fftshift`, `ifftshift`

  Shift the zero-frequency component to the center of the spectrum and back, respectively (more about that soon).

- `fftfreq`

  Return the DFT sample frequencies.

- `rfft`

  Compute the DFT of a real sequence, exploiting the symmetry of the resulting spectrum for increased performance. Also used by `fft` internally when applicable.

This list is complemented by the following functions in NumPy:

- `np.hanning`, `np.hamming`, `np.bartlett`, `np.blackman`, `np.kaiser`

  Tapered windowing functions.

The DFT is also used to perform fast convolutions of large inputs by `scipy.signal.fftconvolve`.

SciPy wraps the Fortran FFTPACK library—it is not the fastest out there, but unlike packages such as FFTW, it has a permissive free software license.

```

**参考**

1. [4. Frequency and the Fast Fourier Transform - Elegant SciPy [Book]](https://www.oreilly.com/library/view/elegant-scipy/9781491922927/ch04.html)
