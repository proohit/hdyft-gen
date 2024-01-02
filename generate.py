from multiprocessing import Pool
import os
import urllib.request
import PIL
import matplotlib.pyplot as plt

from tqdm import tqdm


COLS = 3
ROWS = 3


fig, axs = plt.subplots(ROWS, COLS)

CATAAS_BASE = "https://cataas.com/cat"


def download_image(_):
    return PIL.Image.open(urllib.request.urlopen(CATAAS_BASE))


def draw_image(img, i):
    col = i // COLS
    row = i % COLS
    axs[col, row].imshow(img, aspect="auto")
    axs[col, row].text(
        0.5,
        -0.15,
        i + 1,
        size=12,
        ha="center",
        transform=axs[col, row].transAxes,
    )
    axs[col, row].axis("off")


NUM_IMAGES = COLS * ROWS
if __name__ == "__main__":
    max_workers = os.cpu_count() // 2
    with Pool(max_workers) as pool:
        images = list(
            tqdm(
                pool.imap_unordered(download_image, range(NUM_IMAGES)),
                total=NUM_IMAGES,
                desc="Downloading images",
                unit="image",
            )
        )

    for i, img in tqdm(enumerate(images), desc="Drawing images", unit="image"):
        draw_image(img, i)
    plt.savefig("cats.png", transparent=False, bbox_inches="tight")
