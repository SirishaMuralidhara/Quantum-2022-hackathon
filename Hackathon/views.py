from flask import Blueprint,render_template, request, url_for, flash, redirect,json
import os
from werkzeug.utils import secure_filename
from resume_parser import resumeparse
import pymongo
import spacy
from pdfminer.high_level import extract_text
import numpy as np
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cgi

nlp = spacy.load('en_core_web_sm')


city_info = {

'Andhra Pradesh (AP)':[
			'Adilabad',
			'Anantapur',
			'Chittoor',
			'Kakinada',
			'Guntur',
			'Hyderabad',
			'Karimnagar',
			'Khammam',
			'Krishna',
			'Kurnool',
			'Mahbubnagar',
			'Medak',
			'Nalgonda',
			'Nizamabad',
			'Ongole',
			'Hyderabad',
			'Srikakulam',
			'Nellore',
			'Visakhapatnam',
			'Vizianagaram',
			'Warangal',
			'Eluru',
			'Kadapa',
		],
'Arunachal Pradesh (AR)':[
			'Anjaw',
			'Changlang',
			'East Siang',
			'Kurung Kumey',
			'Lohit',
			'Lower Dibang Valley',
			'Lower Subansiri',
			'Papum Pare',
			'Tawang',
			'Tirap',
			'Dibang Valley',
			'Upper Siang',
			'Upper Subansiri',
			'West Kameng',
			'West Siang',
	],
'Assam (AS)':[
			'Baksa',
			'Barpeta',
			'Bongaigaon',
			'Cachar',
			'Chirang',
			'Darrang',
			'Dhemaji',
			'Dima Hasao',
			'Dhubri',
			'Dibrugarh',
			'Goalpara',
			'Golaghat',
			'Hailakandi',
			'Jorhat',
			'Kamrup',
			'Kamrup Metropolitan',
			'Karbi Anglong',
			'Karimganj',
			'Kokrajhar',
			'Lakhimpur',
			'Marigaon',
			'Nagaon',
			'Nalbari',
			'Sibsagar',
			'Sonitpur',
			'Tinsukia',
			'Udalguri',
	],
'Bihar (BR)':[
			'Araria',
			'Arwal',
			'Aurangabad',
			'Banka',
			'Begusarai',
			'Bhagalpur',
			'Bhojpur',
			'Buxar',
			'Darbhanga',
			'East Champaran',
			'Gaya',
			'Gopalganj',
			'Jamui',
			'Jehanabad',
			'Kaimur',
			'Katihar',
			'Khagaria',
			'Kishanganj',
			'Lakhisarai',
			'Madhepura',
			'Madhubani',
			'Munger',
			'Muzaffarpur',
			'Nalanda',
			'Nawada',
			'Patna',
			'Purnia',
			'Rohtas',
			'Saharsa',
			'Samastipur',
			'Saran',
			'Sheikhpura',
			'Sheohar',
			'Sitamarhi',
			'Siwan',
			'Supaul',
			'Vaishali',
			'West Champaran',
			'Chandigarh',
	],
'Chhattisgarh (CG)':[
			'Bastar',
			'Bijapur',
			'Bilaspur',
			'Dantewada',
			'Dhamtari',
			'Durg',
			'Jashpur',
			'Janjgir-Champa',
			'Korba',
			'Koriya',
			'Kanker',
			'Kabirdham (Kawardha)',
			'Mahasamund',
			'Narayanpur',
			'Raigarh',
			'Rajnandgaon',
			'Raipur',
			'Surguja',
	],
'Dadra and Nagar Haveli (DN)':[
			'Dadra and Nagar Haveli'
],
'Daman and Diu (DD)':[
			'Daman',
			'Diu',
],
'Delhi (DL)':[
			'Central Delhi',
			'East Delhi',
			'New Delhi',
			'North Delhi',
			'North East Delhi',
			'North West Delhi',
			'South Delhi',
			'South West Delhi',
			'West Delhi',
],
'Goa (GA)':[
			'North Goa',
			'South Goa'
],
'Gujarat (GJ)':[
			'Ahmedabad',
			'Amreli district',
			'Anand',
			'Banaskantha',
			'Bharuch',
			'Bhavnagar',
			'Dahod',
			'The Dangs',
			'Gandhinagar',
			'Jamnagar',
			'Junagadh',
			'Kutch',
			'Kheda',
			'Mehsana',
			'Narmada',
			'Navsari',
			'Patan',
			'Panchmahal',
			'Porbandar',
			'Rajkot',
			'Sabarkantha',
			'Surendranagar',
			'Surat',
			'Vyara',
			'Vadodara',
			'Valsad',
],
'Haryana (HR)':[
			'Ambala',
			'Bhiwani',
			'Faridabad',
			'Fatehabad',
			'Gurgaon',
			'Hissar',
			'Jhajjar',
			'Jind',
			'Karnal',
			'Kaithal',
			'Kurukshetra',
			'Mahendragarh',
			'Mewat',
			'Palwal',
			'Panchkula',
			'Panipat',
			'Rewari',
			'Rohtak',
			'Sirsa',
			'Sonipat',
			'Yamuna Nagar',
	],
'Himachal Pradesh (HP)':[
			'Bilaspur',
			'Chamba',
			'Hamirpur',
			'Kangra',
			'Kinnaur',
			'Kullu',
			'Lahaul and Spiti',
			'Mandi',
			'Shimla',
			'Sirmaur',
			'Solan',
			'Una',
	],
'Jammu and Kashmir (JK)':[
			'Anantnag',
			'Badgam',
			'Bandipora',
			'Baramulla',
			'Doda',
			'Ganderbal',
			'Jammu',
			'Kargil',
			'Kathua',
			'Kishtwar',
			'Kupwara',
			'Kulgam',
			'Leh',
			'Poonch',
			'Pulwama',
			'Rajauri',
			'Ramban',
			'Reasi',
			'Samba',
			'Shopian',
			'Srinagar',
			'Udhampur',
	],
'Jharkhand (JH)':[
			'Bokaro',
			'Chatra',
			'Deoghar',
			'Dhanbad',
			'Dumka',
			'East Singhbhum',
			'Garhwa',
			'Giridih',
			'Godda',
			'Gumla',
			'Hazaribag',
			'Jamtara',
			'Khunti',
			'Koderma',
			'Latehar',
			'Lohardaga',
			'Pakur',
			'Palamu',
			'Ramgarh',
			'Ranchi',
			'Sahibganj',
			'Seraikela Kharsawan',
			'Simdega',
			'West Singhbhum',
	],
'Karnataka (KA)':[
			'Bagalkot',
			'Bengaluru',
			'Bangalore Urban',
			'Belgaum',
			'Bellary',
			'Bidar',
			'Bijapur',
			'Chamarajnagar',
			'Chikkamagaluru',
			'Chikkaballapur',
			'Chitradurga',
			'Davanagere',
			'Dharwad',
			'Dakshina Kannada',
			'Gadag',
			'Gulbarga',
			'Hassan',
			'Haveri district',
			'Kodagu',
			'Kolar',
			'Koppal',
			'Mandya',
			'Mysore',
			'Raichur',
			'Shimoga',
			'Tumkur',
			'Udupi',
			'Uttara Kannada',
			'Ramanagara',
			'Yadgir',
	],
'Kerala (KL)':[
			'Alappuzha',
			'Ernakulam',
			'Idukki',
			'Kannur',
			'Kasaragod',
			'Kollam',
			'Kottayam',
			'Kozhikode',
			'Malappuram',
			'Palakkad',
			'Pathanamthitta',
			'Thrissur',
			'Thiruvananthapuram',
			'Wayanad',
	],
'Madhya Pradesh (MP)':[
			'Alirajpur',
			'Anuppur',
			'Ashok Nagar',
			'Balaghat',
			'Barwani',
			'Betul',
			'Bhind',
			'Bhopal',
			'Burhanpur',
			'Chhatarpur',
			'Chhindwara',
			'Damoh',
			'Datia',
			'Dewas',
			'Dhar',
			'Dindori',
			'Guna',
			'Gwalior',
			'Harda',
			'Hoshangabad',
			'Indore',
			'Jabalpur',
			'Jhabua',
			'Katni',
			'Khandwa (East Nimar)',
			'Khargone (West Nimar)',
			'Mandla',
			'Mandsaur',
			'Morena',
			'Narsinghpur',
			'Neemuch',
			'Panna',
			'Rewa',
			'Rajgarh',
			'Ratlam',
			'Raisen',
			'Sagar',
			'Satna',
			'Sehore',
			'Seoni',
			'Shahdol',
			'Shajapur',
			'Sheopur',
			'Shivpuri',
			'Sidhi',
			'Singrauli',
			'Tikamgarh',
			'Ujjain',
			'Umaria',
			'Vidisha',
	],
'Maharashtra (MH)':[
			'Ahmednagar',
			'Akola',
			'Amravati',
			'Aurangabad',
			'Bhandara',
			'Beed',
			'Buldhana',
			'Chandrapur',
			'Dhule',
			'Gadchiroli',
			'Gondia',
			'Hingoli',
			'Jalgaon',
			'Jalna',
			'Kolhapur',
			'Latur',
			'Mumbai City',
			'Mumbai suburban',
			'Nandurbar',
			'Nanded',
			'Nagpur',
			'Nashik',
			'Osmanabad',
			'Parbhani',
			'Pune',
			'Raigad',
			'Ratnagiri',
			'Sindhudurg',
			'Sangli',
			'Solapur',
			'Satara',
			'Thane',
			'Wardha',
			'Washim',
			'Yavatmal',
		],
'Manipur (MN)':[
			'Bishnupur',
			'Churachandpur',
			'Chandel',
			'Imphal East',
			'Senapati',
			'Tamenglong',
			'Thoubal',
			'Ukhrul',
			'Imphal West',
	],
'Meghalaya (ML)':[
			'East Garo Hills',
			'East Khasi Hills',
			'Jaintia Hills',
			'Ri Bhoi',
			'South Garo Hills',
			'West Garo Hills',
			'West Khasi Hills',
	],
'Mizoram (MZ)':[
			'Aizawl',
			'Champhai',
			'Kolasib',
			'Lawngtlai',
			'Lunglei',
			'Mamit',
			'Saiha',
			'Serchhip',
	],
'Nagaland (NL)':[
			'Dimapur',
			'Kohima',
			'Mokokchung',
			'Mon',
			'Phek',
			'Tuensang',
			'Wokha',
			'Zunheboto',
	],
'Orissa (OR)':[
			'Angul',
			'Boudh (Bauda)',
			'Bhadrak',
			'Balangir',
			'Bargarh (Baragarh)',
			'Balasore',
			'Cuttack',
			'Debagarh (Deogarh)',
			'Dhenkanal',
			'Ganjam',
			'Gajapati',
			'Jharsuguda',
			'Jajpur',
			'Jagatsinghpur',
			'Khordha',
			'Kendujhar (Keonjhar)',
			'Kalahandi',
			'Kandhamal',
			'Koraput',
			'Kendrapara',
			'Malkangiri',
			'Mayurbhanj',
			'Nabarangpur',
			'Nuapada',
			'Nayagarh',
			'Puri',
			'Rayagada',
			'Sambalpur',
			'Subarnapur (Sonepur)',
			'Sundergarh',
		],
'Pondicherry (Puducherry) (PY)':[
			'Karaikal',
			'Mahe',
			'Pondicherry',
			'Yanam',
],
'Punjab (PB)':[
			'Amritsar',
			'Barnala',
			'Bathinda',
			'Firozpur',
			'Faridkot',
			'Fatehgarh Sahib',
			'Fazilka',
			'Gurdaspur',
			'Hoshiarpur',
			'Jalandhar',
			'Kapurthala',
			'Ludhiana',
			'Mansa',
			'Moga',
			'Sri Muktsar Sahib',
			'Pathankot',
			'Patiala',
			'Rupnagar',
			'Ajitgarh (Mohali)',
			'Sangrur',
			'Nawanshahr',
			'Tarn Taran',
	],
'Rajasthan (RJ)':[
			'Ajmer',
			'Alwar',
			'Bikaner',
			'Barmer',
			'Banswara',
			'Bharatpur',
			'Baran',
			'Bundi',
			'Bhilwara',
			'Churu',
			'Chittorgarh',
			'Dausa',
			'Dholpur',
			'Dungapur',
			'Ganganagar',
			'Hanumangarh',
			'Jhunjhunu',
			'Jalore',
			'Jodhpur',
			'Jaipur',
			'Jaisalmer',
			'Jhalawar',
			'Karauli',
			'Kota',
			'Nagaur',
			'Pali',
			'Pratapgarh',
			'Rajsamand',
			'Sikar',
			'Sawai Madhopur',
			'Sirohi',
			'Tonk',
			'Udaipur',
	],
'Sikkim (SK)':[
			'East Sikkim',
			'North Sikkim',
			'South Sikkim',
			'West Sikkim',
	],
'Tamil Nadu (TN)':[
			'Ariyalur',
			'Chennai',
			'Coimbatore',
			'Cuddalore',
			'Dharmapuri',
			'Dindigul',
			'Erode',
			'Kanchipuram',
			'Kanyakumari',
			'Karur',
			'Madurai',
			'Nagapattinam',
			'Nilgiris',
			'Namakkal',
			'Perambalur',
			'Pudukkottai',
			'Ramanathapuram',
			'Salem',
			'Sivaganga',
			'Tirupur',
			'Tiruchirappalli',
			'Theni',
			'Tirunelveli',
			'Thanjavur',
			'Thoothukudi',
			'Tiruvallur',
			'Tiruvarur',
			'Tiruvannamalai',
			'Vellore',
			'Viluppuram',
			'Virudhunagar',
	],
'Tripura (TR)':[
			'Dhalai',
			'North Tripura',
			'South Tripura',
			'Khowai',
			'West Tripura',
	],
'Uttar Pradesh (UP)':[
			'Agra',
			'Allahabad',
			'Aligarh',
			'Ambedkar Nagar',
			'Auraiya',
			'Azamgarh',
			'Barabanki',
			'Budaun',
			'Bagpat',
			'Bahraich',
			'Bijnor',
			'Ballia',
			'Banda',
			'Balrampur',
			'Bareilly',
			'Basti',
			'Bulandshahr',
			'Chandauli',
			'Chhatrapati Shahuji Maharaj Nagar',
			'Chitrakoot',
			'Deoria',
			'Etah',
			'Kanshi Ram Nagar',
			'Etawah',
			'Firozabad',
			'Farrukhabad',
			'Fatehpur',
			'Faizabad',
			'Gautam Buddh Nagar',
			'Gonda',
			'Ghazipur',
			'Gorakhpur',
			'Ghaziabad',
			'Hamirpur',
			'Hardoi',
			'Mahamaya Nagar',
			'Jhansi',
			'Jalaun',
			'Jyotiba Phule Nagar',
			'Jaunpur district',
			'Ramabai Nagar (Kanpur Dehat)',
			'Kannauj',
			'Kanpur',
			'Kaushambi',
			'Kushinagar',
			'Lalitpur',
			'Lakhimpur Kheri',
			'Lucknow',
			'Mau',
			'Meerut',
			'Maharajganj',
			'Mahoba',
			'Mirzapur',
			'Moradabad',
			'Mainpuri',
			'Mathura',
			'Muzaffarnagar',
			'Panchsheel Nagar district (Hapur)',
			'Pilibhit',
			'Shamli',
			'Pratapgarh',
			'Rampur',
			'Raebareli',
			'Saharanpur',
			'Sitapur',
			'Shahjahanpur',
			'Sant Kabir Nagar',
			'Siddharthnagar',
			'Sonbhadra',
			'Sant Ravidas Nagar',
			'Sultanpur',
			'Shravasti',
			'Unnao',
			'Varanasi',
	],
'Uttarakhand (UK)':[
			'Almora',
			'Bageshwar',
			'Chamoli',
			'Champawat',
			'Dehradun',
			'Haridwar',
			'Nainital',
			'Pauri Garhwal',
			'Pithoragarh',
			'Rudraprayag',
			'Tehri Garhwal',
			'Udham Singh Nagar',
			'Uttarkashi',
	],
'West Bengal (WB)':[
			'Birbhum',
			'Bankura',
			'Bardhaman',
			'Darjeeling',
			'Dakshin Dinajpur',
			'Hooghly',
			'Howrah',
			'Jalpaiguri',
			'Cooch Behar',
			'Kolkata',
			'Maldah',
			'Paschim Medinipur',
			'Purba Medinipur',
			'Murshidabad',
			'Nadia',
			'North 24 Parganas',
			'South 24 Parganas',
			'Purulia',
			'Uttar Dinajpur',
	]
}

states = list(city_info.keys())


try:
    client = pymongo.MongoClient("mongodb://localhost:27017")
except Exception:
    print("Error : ",Exception)

mydb=client['Hackathon']
myCollection=mydb["resume"]




UPLOAD_FOLDER = 'C:/Users/Public/Hackathon/resumes'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','docx'}



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

views = Blueprint(__name__,"views")

@views.route("/")
def loadHome():
    return render_template("home.html")

@views.route("/candidate")
def loadCandidate():
    return render_template("candidate.html")

@views.route("/recruiter",methods=['GET','POST'])
def loadRecruiter():
    if request.method == 'GET':
        return render_template("recruiter.html")
    if request.method == 'POST':
        res = request.form
        req_skills = res.get('skills').split(',')
        req_city = res.get('city')
        req_state = res.get('state')
        req_min = res.get('min')
        req_max = res.get('max')

        first=[]
        second=[]
        third=[]
        fourth=[]
        fifth = []

        found = myCollection.find({})
        ids=[]
        locations=[]
        skills=[]
        exp=[]
        names=[]
        phones=[]
        emails=[]
        files=[]

        for data in found:
            locations.append(data.get('location'))
            skills.append(data.get('skills'))
            exp.append(data.get('total_exp'))
            ids.append(data.get('_id'))
            names.append(data.get('name'))
            phones.append(data.get('phone'))
            emails.append(data.get('email'))
            files.append(data.get('file'))

        for i in range(len(ids)):

            if locations[i] == req_city and exp[i] >= int(req_min) and exp[i] <= int(req_max) and all(item in skills[i] for item in req_skills):
                first.append(i)
            else:
                if all(item in skills[i] for item in req_skills) and exp[i] >= int(req_min) and exp[i] <= int(req_max):
                    second.append(i)
                else:
                    if all(item in skills[i] for item in req_skills) and locations[i] == req_city:
                        third.append(i)
                    else:
                        if all(item in skills[i] for item in req_skills) and exp[i] >=int(req_min):
                            fourth.append(i)
                        else:
                            if all(item in skills[i] for item in req_skills):
                                fifth.append(i)
        order = first+second+third+fourth+fifth
        nameList = [names[x] for x in order]
        phoneList = [phones[x] for x in order]
        emailList = [emails[x] for x in order]
        fileList = [files[x] for x in order]
        namee = json.dumps(nameList)
        phonee = json.dumps(phoneList)
        emaill = json.dumps(emailList)
        filee = json.dumps(fileList)
        count = len(nameList)
        return render_template("list.html", nameList = namee , phoneList = phonee , emailList = emaill , fileList = filee,count=count)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'filename' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['filename']
        print(file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            data = resumeparse.read_file('C:/Users/Public/Hackathon/resumes/'+filename)

            def extract_text_from_pdf(pdf_path):
                return extract_text(pdf_path)

            text = extract_text_from_pdf('C:/Users/Public/Hackathon/resumes/'+filename)

        
            a=set(text.split())
            exist=[]
            for i in states:
                if(a & set(city_info.get(i))):
                    exist.append(list(a & set(city_info.get(i)))[0])
            print(exist)

            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in ['GPE', 'LOC']:
                    temp = ent.text
            if exist:
                city=exist[0]
            else:
                city=''
            mydoc={
                "name" : data.get('name'),
                "email" : data.get('email'),
                "phone" : data.get('phone'),
                "designation": data.get('designation'),
                "degree" : data.get('degree'),
                "skills" : data.get('skills'),
                "total_exp" : data.get('total_exp'),
                "university" : data.get('university'),
                "companies worked at" : data.get('Companies worked at'),
                "location" : city,
                "file" : filename
            }

            res = myCollection.insert_one(mydoc)
            print(res.inserted_id)

            return "Successfully submitted"

        
    else:
        return "Not a post"
    return ".."




'''@views.route("/",methods=('GET', 'POST'))
def upload():
    if(request.method == 'POST'):
        title = request.form['title']
    if not title:
            flash('Resume is required!')
    else:
        return "Resume uploaded"'''
        