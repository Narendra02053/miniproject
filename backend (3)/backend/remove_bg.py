from PIL import Image
import numpy as np

def remove_background(input_path, output_path, tolerance=30):
    print(f"Processing {input_path}...")
    try:
        img = Image.open(input_path)
        img = img.convert("RGBA")
        
        datas = img.getdata()
        
        # Get the background color from the top-left pixel
        bg_color = datas[0]
        print(f"Detected background color: {bg_color}")
        
        newData = []
        for item in datas:
            # Check if pixel is close to background color
            if all(abs(item[i] - bg_color[i]) < tolerance for i in range(3)):
                newData.append((255, 255, 255, 0))  # Transparent
            else:
                newData.append(item)
        
        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"Saved transparent image to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

input_file = r"c:\Users\knare\Downloads\memorydecaystudy-main\memorydecaystudy-main\frontend (2)\frontend\public\vecna_full.png"
output_file = r"c:\Users\knare\Downloads\memorydecaystudy-main\memorydecaystudy-main\frontend (2)\frontend\public\vecna_transparent.png"

remove_background(input_file, output_file)
