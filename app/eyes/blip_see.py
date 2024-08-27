import replicate

from app import consts

replicate = replicate.Client(api_token=consts.REPLICATE_API_TOKEN)

def blip_see(image_url):

    output = replicate.run(
        "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
        input={
            "task": "image_captioning",
            "image": image_url
        })
    return output



if __name__=="__main__":
    blip_see("https://replicate.delivery/mgxm/f4e50a7b-e8ca-432f-8e68-082034ebcc70/demo.jpg")