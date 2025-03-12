from PIL import Image
import struct
import sys

def convert_bmp_to_raw(bmp_filename, raw_filename):
    # Open the BMP image
    with Image.open(bmp_filename) as img:
        # Convert to RGB (in case it's not already)
        img = img.convert("RGB")

        width, height = img.size
        print(f"Converting {bmp_filename} ({width}x{height}) to {raw_filename}...")

        # Open output file in binary write mode
        with open(raw_filename, "wb") as raw_file:
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))

                    # Convert to RGB565
                    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

                    # Write as big-endian (high byte first, low byte second)
                    raw_file.write(struct.pack(">H", rgb565))

        print(f"Conversion complete! RAW file saved as {raw_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bmp_to_raw.py <input.bmp> <output.raw>")
        sys.exit(1)

    bmp_filename = sys.argv[1]
    raw_filename = sys.argv[2]

    convert_bmp_to_raw(bmp_filename, raw_filename)
