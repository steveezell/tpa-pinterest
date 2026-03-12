# TPA Pinterest Assets

Pinterest pin images and generation scripts for [The Period Academy](https://theperiodacademy.com).

## Structure

```
images/
  YYYY/
    MM/
      pin-[slug]-[variant]-YYYYMMDD.png
scripts/
  generate_pins_YYYYMMDD.py   ← Pillow generation script for each day
pin-log/
  pin-log.json                ← Tracks all posted pins (prevents 30-day repeats)
```

## Workflow

1. Run `scripts/generate_pins_YYYYMMDD.py` to generate 3 pins (1000×1500px)
2. Commit and push images to this repo
3. Upload images directly to Pinterest pin builder (no web hosting required)
4. Update `pin-log/pin-log.json` and commit

## Brand Colors

| Name | Hex | RGB |
|------|-----|-----|
| Periwinkle | #788BFF | (120, 139, 255) |
| Hard Pink | #E8425D | (232, 66, 93) |
| Soft Pink | #F7B4C1 | (247, 180, 193) |
| Slate Blue | #898DAA | (137, 141, 170) |
| Soft Yellow | #FFFB78 | (255, 251, 120) |
| Electric Blue | #78D1FF | (120, 209, 255) |
| Tangerine | #FFE078 | (255, 224, 120) |
