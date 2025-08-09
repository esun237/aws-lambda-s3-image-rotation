import boto3
import os
import io
from PIL import Image, ImageOps

s3 = boto3.client("s3")

BUCKET = os.environ["BUCKET_NAME"]
OUTPUT_PREFIX = os.environ.get("OUTPUT_PREFIX", "output/")


def lambda_handler(event, context):
    for record in event.get("Records", []):
        src_bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        if not key.startswith("incoming/"):
            continue

        filename = key.split("/", 1)[1] if "/" in key else key
        dst_key = f"{OUTPUT_PREFIX}{filename}"

        try:
            obj = s3.get_object(Bucket=src_bucket, Key=key)
            body = obj["Body"].read()

            with Image.open(io.BytesIO(body)) as img:
                try:
                    img = ImageOps.exif_transpose(img)
                except Exception:
                    pass

                rotated = img.rotate(-90, expand=True)

                fmt = (img.format or "JPEG").upper()
                if fmt not in ("JPEG", "PNG", "WEBP", "TIFF", "BMP"):
                    fmt = "JPEG"

                out = io.BytesIO()
                save_kwargs = {}
                if fmt == "JPEG":
                    save_kwargs.update({"quality": 90, "optimize": True})
                rotated.save(out, format=fmt, **save_kwargs)
                out.seek(0)

                content_type = {
                    "JPEG": "image/jpeg",
                    "PNG": "image/png",
                    "WEBP": "image/webp",
                    "TIFF": "image/tiff",
                    "BMP": "image/bmp"
                }.get(fmt, "application/octet-stream")

                s3.put_object(
                    Bucket=BUCKET, 
                    Key=dst_key, 
                    Body=out.getvalue(), 
                    ContentType=content_type,
                    Metadata={"x-rotated": "90"})

        except Exception as e:
            print(f"[ERROR] {key}: {e}")

    return {"statusCode": 200}  # "ok" should be 200
