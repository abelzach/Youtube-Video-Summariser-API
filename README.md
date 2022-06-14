# Youtube-Video-Summariser-API

Using this API you can easily obtain the summarised transcripts from a youtube video link.
Given the youtube video url as a request parameter the api gives the summarised contents(1/10th the size) along with the entire youtube transcripts.

Endpoint :  https://ytvideosummariser.herokuapp.com/api

Request Parameters: 
{

        "url": youtube video link

}    

Usage : https://ytvideosummariser.herokuapp.com/api?url= insert youtube video link here
  
Usage example : https://ytvideosummariser.herokuapp.com/api?url=https://www.youtube.com/watch?v=bz7yYu_w2HY

Output (json format):

{

 "Message": sum marised contents ,
 
 "Transcripts": entire youtube video transcripts
 
}

Kindly message if you are facing any issues
