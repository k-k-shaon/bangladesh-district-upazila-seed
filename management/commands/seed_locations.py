from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import District, Upazila


class Command(BaseCommand):
    help = "Seed all 64 districts and current 500 upazilas of Bangladesh."

    # ============================================================
    # Bangladesh: 64 Districts + 500 Upazilas
    # Current administrative dataset
    # ============================================================

    BANGLADESH_DATA = {
        # ========================================================
        # DHAKA DIVISION - 13 DISTRICTS
        # ========================================================

        "Dhaka": [
            "Dhamrai",
            "Dohar",
            "Keraniganj",
            "Nawabganj",
            "Savar",
        ],

        "Faridpur": [
            "Alfadanga",
            "Bhanga",
            "Boalmari",
            "Charbhadrasan",
            "Faridpur Sadar",
            "Madhukhali",
            "Nagarkanda",
            "Sadarpur",
            "Saltha",
        ],

        "Gazipur": [
            "Gazipur Sadar",
            "Kaliakair",
            "Kaliganj",
            "Kapasia",
            "Sreepur",
        ],

        "Gopalganj": [
            "Gopalganj Sadar",
            "Kashiani",
            "Kotalipara",
            "Muksudpur",
            "Tungipara",
        ],

        "Kishoreganj": [
            "Austagram",
            "Bajitpur",
            "Bhairab",
            "Hossainpur",
            "Itna",
            "Karimganj",
            "Katiadi",
            "Kishoreganj Sadar",
            "Kuliarchar",
            "Mithamain",
            "Nikli",
            "Pakundia",
            "Tarail",
        ],

        "Madaripur": [
            "Kalkini",
            "Madaripur Sadar",
            "Rajoir",
            "Shibchar",
            "Dasar",
        ],

        "Manikganj": [
            "Daulatpur",
            "Ghior",
            "Harirampur",
            "Manikganj Sadar",
            "Saturia",
            "Shibaloy",
            "Singair",
        ],

        "Munshiganj": [
            "Gazaria",
            "Lohajang",
            "Munshiganj Sadar",
            "Sirajdikhan",
            "Sreenagar",
            "Tongibari",
        ],

        "Narayanganj": [
            "Araihazar",
            "Bandar",
            "Narayanganj Sadar",
            "Rupganj",
            "Sonargaon",
        ],

        "Narsingdi": [
            "Belabo",
            "Monohardi",
            "Narsingdi Sadar",
            "Palash",
            "Raipura",
            "Shibpur",
        ],

        "Rajbari": [
            "Baliakandi",
            "Goalanda",
            "Kalukhali",
            "Pangsha",
            "Rajbari Sadar",
        ],

        "Shariatpur": [
            "Bhedarganj",
            "Damudya",
            "Gosairhat",
            "Naria",
            "Shariatpur Sadar",
            "Zajira",
        ],

        "Tangail": [
            "Basail",
            "Bhuapur",
            "Delduar",
            "Dhanbari",
            "Ghatail",
            "Gopalpur",
            "Kalihati",
            "Madhupur",
            "Mirzapur",
            "Nagarpur",
            "Sakhipur",
            "Tangail Sadar",
        ],

        # ========================================================
        # KHULNA DIVISION - 10 DISTRICTS
        # ========================================================

        "Bagerhat": [
            "Bagerhat Sadar",
            "Chitalmari",
            "Fakirhat",
            "Kachua",
            "Mollahat",
            "Mongla",
            "Moralganj",
            "Rampal",
            "Sharankhola",
        ],

        "Chuadanga": [
            "Alamdanga",
            "Chuadanga Sadar",
            "Damurhuda",
            "Jibannagar",
        ],

        "Jashore": [
            "Abhaynagar",
            "Bagherpara",
            "Chaugachha",
            "Jashore Sadar",
            "Jhikargachha",
            "Keshabpur",
            "Manirampur",
            "Sharsha",
        ],

        "Jhenaidah": [
            "Harinakunda",
            "Jhenaidah Sadar",
            "Kaliganj",
            "Kotchandpur",
            "Maheshpur",
            "Shailkupa",
        ],

        "Khulna": [
            "Batiaghata",
            "Dacope",
            "Dumuria",
            "Dighalia",
            "Koyra",
            "Paikgachha",
            "Phultala",
            "Rupsha",
            "Terokhada",
        ],

        "Kushtia": [
            "Bheramara",
            "Daulatpur",
            "Khoksa",
            "Kumarkhali",
            "Kushtia Sadar",
            "Mirpur",
        ],

        "Magura": [
            "Magura Sadar",
            "Mohammadpur",
            "Shalikha",
            "Sreepur",
        ],

        "Meherpur": [
            "Gangni",
            "Mujibnagar",
            "Meherpur Sadar",
        ],

        "Narail": [
            "Kalia",
            "Lohagara",
            "Narail Sadar",
        ],

        "Satkhira": [
            "Assasuni",
            "Debhata",
            "Kalaroa",
            "Kaliganj",
            "Satkhira Sadar",
            "Shyamnagar",
            "Tala",
        ],

        # ========================================================
        # CHATTOGRAM DIVISION - 11 DISTRICTS
        # ========================================================

        "Bandarban": [
            "Alikadam",
            "Bandarban Sadar",
            "Lama",
            "Naikhongchhari",
            "Rowangchhari",
            "Ruma",
            "Thanchi",
        ],

        "Brahmanbaria": [
            "Akhaura",
            "Ashuganj",
            "Bancharampur",
            "Bijoynagar",
            "Brahmanbaria Sadar",
            "Kasba",
            "Nabinagar",
            "Nasirnagar",
            "Sarail",
        ],

        "Chandpur": [
            "Chandpur Sadar",
            "Faridganj",
            "Haimchar",
            "Hajiganj",
            "Kachua",
            "Matlab Dakshin",
            "Matlab Uttar",
            "Shahrasti",
        ],

        "Chattogram": [
            "Anwara",
            "Banshkhali",
            "Boalkhali",
            "Chandanaish",
            "Fatikchhari",
            "Hathazari",
            "Lohagara",
            "Mirsharai",
            "Patiya",
            "Rangunia",
            "Raozan",
            "Sandwip",
            "Satkania",
            "Sitakunda",
            "Karnaphuli",
        ],

        "Cumilla": [
            "Barura",
            "Brahmanpara",
            "Burichong",
            "Chandina",
            "Chauddagram",
            "Cumilla Adarsha Sadar",
            "Cumilla Sadar Dakshin",
            "Daudkandi",
            "Debidwar",
            "Homna",
            "Laksam",
            "Manoharganj",
            "Meghna",
            "Muradnagar",
            "Nangalkot",
            "Titas",
            "Lalmai",
        ],

        "Cox's Bazar": [
            "Chakaria",
            "Cox's Bazar Sadar",
            "Kutubdia",
            "Maheshkhali",
            "Matamuhuri",
            "Pekua",
            "Ramu",
            "Teknaf",
            "Ukhia",
            "Eidgaon",
        ],

        "Feni": [
            "Chhagalnaiya",
            "Daganbhuiyan",
            "Feni Sadar",
            "Fulagazi",
            "Parshuram",
            "Sonagazi",
        ],

        "Khagrachhari": [
            "Dighinala",
            "Manikchhari",
            "Khagrachhari Sadar",
            "Lakshmichhari",
            "Mahalchhari",
            "Matiranga",
            "Panchhari",
            "Ramgarh",
            "Guimara",
        ],

        "Lakshmipur": [
            "Kamalnagar",
            "Lakshmipur Sadar",
            "Raipur",
            "Ramganj",
            "Ramgati",
            "Chandraganj",
        ],

        "Noakhali": [
            "Begumganj",
            "Chatkhil",
            "Companiganj",
            "Hatiya",
            "Senbagh",
            "Sonaimuri",
            "Subarnachar",
            "Noakhali Sadar",
            "Kabirhat",
        ],

        "Rangamati": [
            "Baghaichhari",
            "Barkal",
            "Belaichhari",
            "Juraichhari",
            "Kaptai",
            "Kawkhali",
            "Langadu",
            "Naniarchar",
            "Rajasthali",
            "Rangamati Sadar",
        ],

        # ========================================================
        # RAJSHAHI DIVISION - 8 DISTRICTS
        # ========================================================

        "Bogura": [
            "Adamdighi",
            "Bogura Sadar",
            "Dhunat",
            "Dupchanchia",
            "Gabtali",
            "Kahaloo",
            "Nandigram",
            "Sariakandi",
            "Shajahanpur",
            "Sherpur",
            "Shibganj",
            "Sonatala",
            "Mokamtola",
        ],

        "Joypurhat": [
            "Akkelpur",
            "Joypurhat Sadar",
            "Kalai",
            "Khetlal",
            "Panchbibi",
        ],

        "Naogaon": [
            "Atrai",
            "Badalgachhi",
            "Dhamoirhat",
            "Manda",
            "Mahadebpur",
            "Naogaon Sadar",
            "Niamatpur",
            "Patnitala",
            "Porsha",
            "Raninagar",
            "Sapahar",
        ],

        "Natore": [
            "Bagatipara",
            "Baraigram",
            "Gurudaspur",
            "Lalpur",
            "Natore Sadar",
            "Singra",
            "Naldanga",
        ],

        "Chapainawabganj": [
            "Bholahat",
            "Gomastapur",
            "Nachole",
            "Chapainawabganj Sadar",
            "Shibganj",
        ],

        "Pabna": [
            "Atgharia",
            "Bera",
            "Bhangura",
            "Chatmohar",
            "Faridpur",
            "Ishwardi",
            "Pabna Sadar",
            "Santhia",
            "Sujanagar",
        ],

        "Rajshahi": [
            "Bagha",
            "Bagmara",
            "Charghat",
            "Durgapur",
            "Godagari",
            "Mohanpur",
            "Paba",
            "Puthia",
            "Tanore",
        ],

        "Sirajganj": [
            "Belkuchi",
            "Chauhali",
            "Kamarkhanda",
            "Kazipur",
            "Raiganj",
            "Shahjadpur",
            "Sirajganj Sadar",
            "Tarash",
            "Ullahpara",
        ],

        # ========================================================
        # SYLHET DIVISION - 4 DISTRICTS
        # ========================================================

        "Habiganj": [
            "Ajmiriganj",
            "Bahubal",
            "Baniachong",
            "Chunarughat",
            "Habiganj Sadar",
            "Lakhai",
            "Madhabpur",
            "Nabiganj",
            "Shayestaganj",
        ],

        "Moulvibazar": [
            "Barlekha",
            "Juri",
            "Kamalganj",
            "Kulaura",
            "Moulvibazar Sadar",
            "Rajnagar",
            "Sreemangal",
        ],

        "Sunamganj": [
            "Bishwamvarpur",
            "Chhatak",
            "Derai",
            "Dharampasha",
            "Dowarabazar",
            "Jagannathpur",
            "Jamalganj",
            "Madhyanagar",
            "Shantiganj",
            "Shalla",
            "Sunamganj Sadar",
            "Tahirpur",
        ],

        "Sylhet": [
            "Balaganj",
            "Beanibazar",
            "Bishwanath",
            "Companiganj",
            "Dakshin Surma",
            "Fenchuganj",
            "Golapganj",
            "Gowainghat",
            "Jaintiapur",
            "Kanaighat",
            "Osmani Nagar",
            "Sylhet Sadar",
            "Zakiganj",
        ],

        # ========================================================
        # RANGPUR DIVISION - 8 DISTRICTS
        # ========================================================

        "Dinajpur": [
            "Birampur",
            "Birganj",
            "Biral",
            "Bochaganj",
            "Chirirbandar",
            "Phulbari",
            "Ghoraghat",
            "Hakimpur",
            "Kaharole",
            "Khansama",
            "Nawabganj",
            "Parbatipur",
            "Dinajpur Sadar",
        ],

        "Gaibandha": [
            "Fulchhari",
            "Gaibandha Sadar",
            "Gobindaganj",
            "Palashbari",
            "Sadullapur",
            "Saghata",
            "Sundarganj",
        ],

        "Kurigram": [
            "Phulbari",
            "Bhurungamari",
            "Char Rajibpur",
            "Chilmari",
            "Kurigram Sadar",
            "Nageshwari",
            "Rajarhat",
            "Roumari",
            "Ulipur",
        ],

        "Lalmonirhat": [
            "Aditmari",
            "Hatibandha",
            "Kaliganj",
            "Lalmonirhat Sadar",
            "Patgram",
        ],

        "Nilphamari": [
            "Domar",
            "Jaldhaka",
            "Kishoreganj",
            "Nilphamari Sadar",
            "Saidpur",
            "Dimla",
        ],

        "Panchagarh": [
            "Atwari",
            "Boda",
            "Debiganj",
            "Panchagarh Sadar",
            "Tetulia",
        ],

        "Rangpur": [
            "Badarganj",
            "Kaunia",
            "Rangpur Sadar",
            "Mithapukur",
            "Pirganj",
            "Pirgachha",
            "Taraganj",
            "Gangachara",
        ],

        "Thakurgaon": [
            "Pirganj",
            "Baliadangi",
            "Haripur",
            "Ranisankail",
            "Thakurgaon Sadar",
            "Bhully",
            "Ruhia",
        ],

        # ========================================================
        # MYMENSINGH DIVISION - 4 DISTRICTS
        # ========================================================

        "Jamalpur": [
            "Baksiganj",
            "Dewanganj",
            "Islampur",
            "Jamalpur Sadar",
            "Madarganj",
            "Melandaha",
            "Sarishabari",
        ],

        "Mymensingh": [
            "Bhaluka",
            "Dhobaura",
            "Fulbaria",
            "Gaffargaon",
            "Gauripur",
            "Haluaghat",
            "Ishwarganj",
            "Muktagachha",
            "Mymensingh Sadar",
            "Nandail",
            "Phulpur",
            "Tarakanda",
            "Trishal",
        ],

        "Netrokona": [
            "Atpara",
            "Barhatta",
            "Durgapur",
            "Khaliajuri",
            "Kalmakanda",
            "Kendua",
            "Madan",
            "Mohanganj",
            "Netrokona Sadar",
            "Purbadhala",
        ],

        "Sherpur": [
            "Jhenaigati",
            "Nakla",
            "Nalitabari",
            "Sherpur Sadar",
            "Sreebardi",
        ],

        # ========================================================
        # BARISHAL DIVISION - 6 DISTRICTS
        # ========================================================

        "Barguna": [
            "Amtali",
            "Bamna",
            "Barguna Sadar",
            "Betagi",
            "Patharghata",
            "Taltali",
        ],

        "Barishal": [
            "Agailjhara",
            "Babuganj",
            "Bakerganj",
            "Banaripara",
            "Gournadi",
            "Hizla",
            "Barishal Sadar",
            "Mehendiganj",
            "Muladi",
            "Wazirpur",
        ],

        "Bhola": [
            "Bhola Sadar",
            "Borhanuddin",
            "Char Fasson",
            "Daulatkhan",
            "Lalmohan",
            "Manpura",
            "Tazumuddin",
        ],

        "Jhalokathi": [
            "Jhalokathi Sadar",
            "Kathalia",
            "Nalchity",
            "Rajapur",
        ],

        "Patuakhali": [
            "Bauphal",
            "Dashmina",
            "Dumki",
            "Kalapara",
            "Mirzaganj",
            "Patuakhali Sadar",
            "Rangabali",
            "Galachipa",
        ],

        "Pirojpur": [
            "Bhandaria",
            "Kawkhali",
            "Mathbaria",
            "Nazirpur",
            "Pirojpur Sadar",
            "Nesarabad",
            "Zianagar",
        ],
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "--clean",
            action="store_true",
            help=(
                "Remove location records that are not part of the "
                "current 64-district/500-upazila dataset."
            ),
        )

    def handle(self, *args, **options):
        clean = options["clean"]

        # --------------------------------------------------------
        # Validation BEFORE touching the database
        # --------------------------------------------------------

        district_count = len(self.BANGLADESH_DATA)

        if district_count != 64:
            raise CommandError(
                f"Dataset validation failed: "
                f"expected 64 districts, found {district_count}."
            )

        total_upazilas = sum(
            len(upazilas)
            for upazilas in self.BANGLADESH_DATA.values()
        )

        if total_upazilas != 500:
            raise CommandError(
                f"Dataset validation failed: "
                f"expected 500 upazilas, found {total_upazilas}."
            )

        # Check duplicate district names
        district_names = list(self.BANGLADESH_DATA.keys())

        if len(district_names) != len(set(district_names)):
            raise CommandError(
                "Dataset validation failed: duplicate district found."
            )

        # Check duplicate upazila inside each district
        for district_name, upazilas in self.BANGLADESH_DATA.items():
            if len(upazilas) != len(set(upazilas)):
                duplicates = sorted(
                    {
                        name
                        for name in upazilas
                        if upazilas.count(name) > 1
                    }
                )

                raise CommandError(
                    f"Duplicate upazila found in {district_name}: "
                    f"{', '.join(duplicates)}"
                )

        self.stdout.write(
            self.style.NOTICE(
                f"Dataset validated: "
                f"{district_count} districts / "
                f"{total_upazilas} upazilas."
            )
        )

        # --------------------------------------------------------
        # Database operation
        # --------------------------------------------------------

        with transaction.atomic():

            existing_districts = {
                district.name: district
                for district in District.objects.all()
            }

            created_districts = 0
            existing_district_count = 0
            created_upazilas = 0
            existing_upazila_count = 0

            for district_name, upazilas in self.BANGLADESH_DATA.items():

                district = existing_districts.get(district_name)

                if district is None:
                    district = District.objects.create(
                        name=district_name
                    )
                    created_districts += 1
                else:
                    existing_district_count += 1

                for upazila_name in upazilas:

                    _, created = Upazila.objects.get_or_create(
                        district=district,
                        name=upazila_name,
                    )

                    if created:
                        created_upazilas += 1
                    else:
                        existing_upazila_count += 1

            # ----------------------------------------------------
            # Optional cleanup
            #
            # Removes old wrong entries such as:
            # Mirpur, Gulshan, Uttara, Tejgaon etc.
            # which were previously stored as "upazila".
            # ----------------------------------------------------

            deleted_upazilas = 0
            deleted_districts = 0

            if clean:

                valid_district_names = set(
                    self.BANGLADESH_DATA.keys()
                )

                valid_upazilas = {
                    (district_name, upazila_name)
                    for district_name, upazilas
                    in self.BANGLADESH_DATA.items()
                    for upazila_name in upazilas
                }

                # Remove stale upazilas
                for upazila in Upazila.objects.select_related(
                    "district"
                ).all():

                    key = (
                        upazila.district.name,
                        upazila.name,
                    )

                    if key not in valid_upazilas:
                        try:
                            upazila.delete()
                            deleted_upazilas += 1
                        except Exception as exc:
                            raise CommandError(
                                f"Could not delete old upazila "
                                f"'{upazila.name}' under "
                                f"'{upazila.district.name}'. "
                                f"It may be referenced by another "
                                f"model. Original error: {exc}"
                            )

                # Remove stale districts
                for district in District.objects.all():

                    if district.name not in valid_district_names:
                        try:
                            district.delete()
                            deleted_districts += 1
                        except Exception as exc:
                            raise CommandError(
                                f"Could not delete old district "
                                f"'{district.name}'. "
                                f"It may be referenced by another "
                                f"model. Original error: {exc}"
                            )

        # --------------------------------------------------------
        # Final database validation
        # --------------------------------------------------------

        final_district_count = District.objects.count()
        final_upazila_count = Upazila.objects.count()

        if final_district_count != 64:
            raise CommandError(
                f"Final database validation failed: "
                f"expected 64 districts, found "
                f"{final_district_count}."
            )

        if final_upazila_count != 500:
            raise CommandError(
                f"Final database validation failed: "
                f"expected 500 upazilas, found "
                f"{final_upazila_count}."
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Location seeding completed successfully!"
            )
        )

        self.stdout.write(
            f"Districts: {final_district_count}/64"
        )

        self.stdout.write(
            f"Upazilas: {final_upazila_count}/500"
        )

        self.stdout.write(
            f"New districts created: {created_districts}"
        )

        self.stdout.write(
            f"Existing districts: {existing_district_count}"
        )

        self.stdout.write(
            f"New upazilas created: {created_upazilas}"
        )

        self.stdout.write(
            f"Existing upazilas: {existing_upazila_count}"
        )

        if clean:
            self.stdout.write(
                f"Old/wrong upazilas removed: {deleted_upazilas}"
            )

            self.stdout.write(
                f"Old/wrong districts removed: {deleted_districts}"
            )