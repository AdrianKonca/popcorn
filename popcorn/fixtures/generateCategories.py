import json

# One off script to generate fixture for categories
# Launch it using
# `python .\popcorn\fixtures\generateCategories.py > categories.json`
# Copy contents categories.json into InitialData.json (between users and recipes)
# Make sure that the json is formatted correctly
# Remove categories.json

categories_data = [
    ["1a.jpg", "Śniadanie", 2],
    ["1b.jpg", "Obiad", 2],
    ["1c.jpg", "Kolacja", 2],
    ["2a.jpg", "Mięsne", 3],
    ["2b.jpg", "Wegetariańskie", 3],
    ["2c.jpg", "Wegańskie", 3],
    ["3a.jpg", "Przystawka", 4],
    ["3b.jpg", "Danie główne", 4],
    ["3c.jpg", "Zupa", 4],
    ["3d.jpg", "Ciasto", 4],
    ["3e.jpg", "Przekąska", 4],
    ["1d.jpg", "Deser", 4],
    ["1e.jpg", "Napój", 4],
    ["4a.jpg", "Słone", 4],
    ["4b.jpg", "Słodkie", 4],
    ["4c.jpg", "Kwaśne", 4], ]


def main():
    MODEL = 'popcorn.category'
    UPLOAD_TO = 'categories/'
    IMAGE_INDEX = 0
    NAME_INDEX = 1
    TAG_INDEX = 2

    categories = []
    for i, category_data in enumerate(categories_data):
        category = {
            "model": MODEL,
            "pk": i + 1,
            "fields": {
                "name": category_data[NAME_INDEX],
                "image": UPLOAD_TO + category_data[IMAGE_INDEX],
                "tag": category_data[TAG_INDEX]
            }
        }
        categories.append(category)
    print(json.dumps(categories, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
