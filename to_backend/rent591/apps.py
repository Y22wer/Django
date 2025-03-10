from django.apps import AppConfig



from .爬蟲 import House591Spider,JobSpider

class Rent591Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rent591'
    def ready(self):
        import threading , time
        from .models import House ,Job
        def run_House591Spider():
            house_spider = House591Spider()
            filter_params = [
                {
                "region":"3",
                "kind":"2",#房屋種類
                "price":"0_5000,5000_9999",
                "notice" : "boy,money_asc"
                },
                {
                "region":"3",
                "kind":"3",#房屋種類
                "price":"0_5000,5000_9999",
                "notice" : "boy,all_sex"
                }
                ]
            sort_params = {
                'sort': 'money_asc'  # 租金由高到低排序
            }

            filter_params_index=len(filter_params)
            
            while True:
                
                filter_params_index= filter_params_index- 1 if filter_params_index > 0 else len(filter_params)-1
                
                new_house_ids = house_spider.search(filter_params[filter_params_index], sort_params)
               
                # 獲取資料庫中的所有房屋 ID
                old_house_ids = set(House.objects.values_list('house_id', flat=True))

                # 找出需要刪除的房屋 ID
                ids_to_delete = old_house_ids - new_house_ids
                House.objects.filter(house_id__in=ids_to_delete).delete()
                
                # 找出需要新增的房屋 ID
                ids_to_add = new_house_ids - old_house_ids
                
                # 新增新的房屋 ID 到資料庫
                for house_id in ids_to_add:
                    House.objects.create(house_id=house_id)
                    
                if ids_to_add:
                    print(f"-*-*-*--*-*-*-{ids_to_add}")
                    house_spider.send_telegram(ids_to_add, 
                    'https://rent.591.com.tw/rent-detail-{}.html',
                    "7860456857:AAEeGAEsSQ1tQuaCjxC4TqkhXs62GCKjsUI",
                    "5298494709"
                    )
                    
                time.sleep(3600)
        # 啟動一個背景執行緒來執行爬蟲任務
        
        def run_JobsSpider():
            jobs_spider = JobSpider()
            filter_params = [
                {'area': 'Tainan', 'categories': '7,8,9,11'},
                {'area': 'Kaohsiung', 'categories': '7,8,9,11'},
                {'keyword': '程式'},
                # {'job_type': 'engineer', 'sort': 'new'}
                ]
            # sort_params = {
            #     'sort': 'new'  #最新
            # }

            filter_params_index=len(filter_params)
            
            while True:
                
                filter_params_index= filter_params_index- 1 if filter_params_index > 0 else len(filter_params)-1
                
                new_jobs_ids = jobs_spider.search(filter_params[filter_params_index])
               
                # 獲取資料庫中的所有房屋 ID
                old_jobs_ids = set(Job.objects.values_list('job_id', flat=True))

                # 找出需要刪除的房屋 ID
                ids_to_delete = old_jobs_ids - new_jobs_ids
                Job.objects.filter(job_id__in=ids_to_delete).delete()
                
                # 找出需要新增的房屋 ID
                ids_to_add = new_jobs_ids - old_jobs_ids
                
                # 新增新的房屋 ID 到資料庫
                for job_id in ids_to_add:
                    Job.objects.create(job_id=job_id)
                    
                if ids_to_add:
                    jobs_spider.send_telegram(
                        ids_to_add, 
                        'https://www.chickpt.com.tw/job-{}',
                        "7860456857:AAEeGAEsSQ1tQuaCjxC4TqkhXs62GCKjsUI",
                        "5298494709"
                    )

                time.sleep(3600)
        # 啟動一個背景執行緒來執行爬蟲任務
        
        def clean_old():
            old_house_ids = set(House.objects.values_list('house_id', flat=True))
            import requests
            while True:
                time.sleep(12*3600)
                for i in old_house_ids:
                    url = f"https://rent.591.com.tw/rent-detail-{i}.html\n"
                    statuscode =requests.get(url).status_code
                    if statuscode    != 200:
                        House.objects.filter(house_id=i).delete()
                    elif statuscode == 405:
                        print(f"house_id {i} is 405")

        # threading.Thread(target=clean_old, daemon=True).start()
        threading.Thread(target=run_House591Spider, daemon=True).start()
        threading.Thread(target=run_JobsSpider, daemon=True).start()