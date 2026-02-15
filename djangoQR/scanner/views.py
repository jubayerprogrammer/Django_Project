from django.shortcuts import render
import cv2
import os,uuid
from scanner.models import qr_code
import qrcode
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from pathlib import Path
from io import BytesIO
from django.http import HttpResponseRedirect



# Create your views here.
def generate_qr(req):
    qr_image_url = None
    if req.method == "POST":
        mobile_number = req.POST.get("mobile_number")
        data = req.POST.get("qr_data")

        if len(mobile_number) != 11 or not mobile_number.isdigit():
            return render(req,"scanner/generate_qr.html",{"error": "Invalid mobile number"})
        
        qr_content = f"{mobile_number} | {data}"
        qr = qrcode.make(qr_content)
        qr_image_io = BytesIO()
        qr.save(qr_image_io,format="PNG")
        qr_image_io.seek(0)

        qr_storage_path = os.path.join(settings.MEDIA_ROOT,"qr_codes")
        fs = FileSystemStorage(location=qr_storage_path,base_url="/media/qr_codes/")
        file_name = f"{mobile_number}_{data}_{uuid.uuid4().hex[0:6]}.png"
        qr_image_content = ContentFile(qr_image_io.read(),name=file_name)
        file_path = fs.save(file_name,qr_image_content)
        qr_image_url = fs.url(file_name)
        qr_code.objects.create(data=data,phon_number = mobile_number)

    return render(req,"scanner/generate_qr.html",{"qr_image_url" : qr_image_url})    


    


def scan_qr(req):
    if req.method == "POST" and req.FILES.get("qr_image"):
        mobile_number =req.POST.get("mobile_number")
        amount = req.POST.get("qr_data")
        qr_image = req.FILES["qr_image"]

        if len(mobile_number) != 11 or not mobile_number.isdigit():
            return render(req,"scanner/scan.html",{"error" : "The phone number is not valid.Place enter valid phone number"})
        fs = FileSystemStorage()
        filename = fs.save(qr_image.name,qr_image)
        image_path = Path(fs.location) / filename
        try:
            image = cv2.imread(str(image_path))
            detector = cv2.QRCodeDetector()
            data,bbox,_ = detector.detectAndDecode(image)

            if data :
                id_number = 0
                id2 = qr_code.objects.values_list("id",flat = True)
                for i in id2:
                    id_number = i

                qr_obj = qr_code(id=id_number,data =data,phon_number = mobile_number)
                qr_obj.delete()
                return render(req,"scanner/scan.html",{"success" : f"your data is {data} " })
            else:
                return render(req,"scanner/scan.html",{"error": "Some thing is not valid .Pleace something is wrong"})
        except Exception as e :
            return render(req,"scanner/scan.html",{"error":f"Error: {str(e)}"})
        
    return render(req,"scanner/scan.html",)



