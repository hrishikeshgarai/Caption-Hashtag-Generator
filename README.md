<b>CAPTION AND HASHTAG GENERATOR</b>

<b>About:</b>
The idea behind this project is that millions of people share photos and videos on social media platforms like Facebook, Instagram and Twitter with some relevant captions and hashtags. To make the search for relevant captions and hashtags easier, Caption and Hashtag Generator can be used which generates captions and hashtags relevant to the image and directly uploads it to social media. The whole process is divided into five steps: Uploading pictures, generating captions, generating hashtags, adding location and mood and finally uploading it to social media.

<b>The application works as follows:</b>
User uploads pictures to be shared on social media. The application fetches the image metadata using the AWS Rekognition API. With the help of metadata as keywords, captions are generated through the Quotes API and displayed it to the user. Here, the user can select one or more relevant captions. Like captions, hashtags are generated using Hashtag API and displayed to the user. On selecting relevant hashtags, mood can be selected from the options available in Facebook. Location is automatically generated using the browser location. Finally, the user can share it to social media platforms.

<b>Tools:</b>
The application is developed using Django in the backend and JavaScript in the frontend. Few AWS components like S3, Rekognition API and Elastic BeanStalk are used. Elastic Search is also used to store the captions and hashtags for future. All APIs used here are REST APIs.

The backend logic can be viewed here:
[Backend](https://github.com/hrishikeshgarai/Caption-Hashtag-Generator/blob/master/uploads/core/views.py)

The frontend logic for various pages can be viewed here:
[Frontend](https://github.com/hrishikeshgarai/Caption-Hashtag-Generator/tree/master/uploads/templates/core)
