# TripAssistant
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Application view](#application-view)
* [Sources](#sources)

## General info
<p>An application that allows searching for places that you are looking for in any city of world. After typing phrases you will get card with:
<li> Place name </li>
<li> Address </li>
<li> Images uploaded by users with option to upload new image </li>
<li> Option to read and add reviews </li>
<li> Link to find place on map in Google Maps </li>
</p>

## Technologies
<ul>
<li>Python</li>
<li>Django</li>
<li>PostgreSQL</li>
<li>HTML</li>
<li>CSS</li>
<li>Bootstrap</li>
<li>Nominatim API</li>
<li>Docker / Docker-Compose</li>
</ul>

## Setup
Info about required keys/data in file .env.dist <br/>
GIT: <br/>
Clone repository
```git clone https://github.com/mmackowsky/TripAssistant.git``` <br/>
Install requirements
```pip install requirements.txt``` <br/>
Make migrations
```python manage.py makemigrations``` -> ```python manage.py migrate``` <br/><br/>

Docker/Docker Compose: <br/>
```docker-compose build``` -> ```docker-compose up```

## Application view
<img src="https://github.com/mmackowsky/TripAssistant/assets/123114901/9489b10b-8006-47ba-9c6e-20623f6ac08c" alt="before search">
<img src="https://github.com/mmackowsky/TripAssistant/assets/123114901/ad8f3b4e-b4b7-49a4-a8cf-23e293bde985" alt="after search">
<img src="https://github.com/mmackowsky/TripAssistant/assets/123114901/96fe55c1-8e85-4e3e-a7e0-e32dab5721fe" alt="with footer">
<img src="https://github.com/mmackowsky/TripAssistant/assets/123114901/e5e9daa2-ed1d-418b-a111-0f9606010834" alt="login">
<img src="https://github.com/mmackowsky/TripAssistant/assets/123114901/8398b9e4-37b2-48ea-af22-f5508f65d780" alt="register">
<img src="https://github.com/mmackowsky/TripAssistant/assets/123114901/065bd09c-1be2-4c58-9f5f-8bc3f6830948" alt="password reset">
<img src="https://github.com/mmackowsky/TripAssistant/assets/123114901/d071bb9b-fe98-44d4-a809-40fcf6e04ec1" alt="reviews">

## Sources
Templates source and inspiration https://colorlib.com, https://codepen.io <br/>
Images downloaded from Google in presentation purpose.
