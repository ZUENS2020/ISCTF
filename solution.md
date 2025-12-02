# CTF Challenge Solution

## Challenge
- **Type**: Misc
- **Hint**: "I know you understand the pixel is very powerful, or let's have a showdown?"
- **Password**: 123456

## Solution

1. Extract the `challenge.zip` file using password `123456`
2. Open the extracted `challenge.png` image
3. The flag is visible directly in the image

## Flag

```
flag{f4k3_s1gn1_in_hhh}
```

## Analysis

The image is a 279x477 pixel PNG with RGBA color mode. The flag text is displayed in the center of the image on a white background. The hint about "pixel" suggested examining the image, but the flag was simply visible in plain text when viewing the image.
