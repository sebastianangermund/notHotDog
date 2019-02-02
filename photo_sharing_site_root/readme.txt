
To test project features:

1. Activate env and install requirements

   $ pip install -r requirements.txt

   $ npm install

2. Create superuser with 

   $ python manage.py createsuperuser

3. Run site with 

   $ python manage.py runserver

4. Open site,login and upload new photo (jpg, png, bmp or gif). This will take
   you to the photos detail page. Keep that open.

5. In a new terminal window, navigate to site root, activate env and run 

   $ python ./classifier/photo_consumer.py

   The terminal will print out some status and the classifier's results.

6. If rhe result for "hotdogs" was <= 0.95 you can refresh the photo's detail 
   page, showing the photo and there should be a text saying that the image 
   doesn't depict a hotdog.

$$ ~~ ---------------- ## //\\//\\ ## ---------------- ~~ $$

To start new app:

1. You need to first create a directory appname inside project

$ mkdir /photo_sharing_site/appname 

2. Then, run the startapp command to create the app.

$ django-admin.py startapp appname ./photo_sharing_site/appname

$$ ~~ ---------------- ## //\\//\\ ## ---------------- ~~ $$

API endpoints:

GET:
api/photos/
api/photos/uuid/

POST:
api/photos/

PUT:
api/photos/uuid/photo/
api/photos/uuid/flagged/

E.g.:

curl -X PUT -d 'flagged=true' --user agge:123Hejsan http://127.0.0.1:8000/api/photos/cf134197-4ed8-4bdf-b322-cc2ba82e6335/flagged/ 

$$ ~~ ---------------- ## //\\//\\ ## ---------------- ~~ $$

Project inspired by:

https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5

http://www.django-rest-framework.org/

https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website

https://stackoverflow.com/questions/10382838/how-to-set-foreignkey-in-createview

https://stackoverflow.com/questions/24201676/how-can-i-test-binary-file-uploading-with-django-rest-frameworks-test-client

https://www.tensorflow.org/hub/tutorials/image_retraining

$$ ~~ ---------------- ## //\\//\\ ## ---------------- ~~ $$

Create photo object from shell:

>>> from django.contrib.auth.models import User
>>> from photo_sharing_site.photos.models import Photo
>>> from django.core.files import File
>>> photoTesting=Photo(title='TestingTesting', description='tortillas', owner=User.objects.get(username='agge'))
>>> photoTesting.photo.save('tortil.jpg', File(open('assets/images/9.jpg', 'rb')))
>>> photoTesting.save()

# Now tortil.jpg should have been placed in location defined in Photo model, and the image
# should be visible at homepage.

$$ ~~ ---------------- ## //\\//\\ ## ---------------- ~~ $$

Clear Rabbit queue:

$ rabbitmqadmin delete queue name=name_of_queue

Clear docker:

docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)