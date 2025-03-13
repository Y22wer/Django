from django.apps import AppConfig
from .爬蟲 import House591Spider,JobSpider
from to_backend.settings import TOKEN ,CHANNEL_ID
import numpy as np
def find_diff_elements_np(list1, list2):
    """
    使用 NumPy 找出兩個串列的不同元素，並保持順序和速度。

    Args:
        list1: 第一個串列。
        list2: 第二個串列。

    Returns:
        一個包含兩個 NumPy 陣列的元組：
            - 第一個陣列包含串列 1 有而串列 2 沒有的元素。
            - 第二個陣列包含串列 2 有而串列 1 沒有的元素。
    """

    arr1 = np.array(list1)
    arr2 = np.array(list2)

    # 找出串列 1 有而串列 2 沒有的元素
    mask1 = np.isin(arr1, arr2, invert=True)
    diff1 = arr1[mask1]

    # 找出串列 2 有而串列 1 沒有的元素
    mask2 = np.isin(arr2, arr1, invert=True)
    diff2 = arr2[mask2]

    return diff1, diff2


class Rent591Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rent591'
    def ready(self):
        self.create_SuperUser()
        import threading , time
        from .models import House ,Job
        def run_House591Spider():
            house_spider = House591Spider()
            filter_params = [
                {
                "region":"3",
                "kind":"2",
                "price":"0$_9999",
                "notice" : "boy,all_sex"
                },
                {
                "region":"3",
                "kind":"3",
                "price":"0$_9999",
                "notice" : "boy,all_sex"
                }
                ]
            sort_params = {
                'sort': 'money_asc' 
            }

            filter_params_index=len(filter_params)
            
            while True:
                
                filter_params_index= filter_params_index- 1 if filter_params_index > 0 else len(filter_params)-1
                
                new_house_ids = house_spider.search(filter_params[filter_params_index], sort_params)
               
                # 獲取資料庫中的所有房屋 ID
                old_house_ids = House.objects.values_list('house_id', flat=True)

                ids_to_delete , ids_to_add=find_diff_elements_np(old_house_ids, new_house_ids)
                
                House.objects.filter(house_id__in=ids_to_delete).delete()
        
                # 新增新的房屋 ID 到資料庫
                for house_id in ids_to_add:
                    House.objects.get_or_create(house_id=house_id)
                    
                if ids_to_add.size > 0:
                    print(f"-*-*-*--*-*-*-{ids_to_add}")
                    house_spider.send_telegram(ids_to_add, 
                    'https://rent.591.com.tw/rent-detail-{}.html',
                    TOKEN ,CHANNEL_ID  )
                    
                time.sleep(1200)
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
               
                # 獲取資料庫中的所有工作 ID
                old_jobs_ids = Job.objects.values_list('job_id', flat=True)

                ids_to_delete , ids_to_add=find_diff_elements_np(old_jobs_ids, new_jobs_ids)
                
                Job.objects.filter(job_id__in=ids_to_delete).delete()
                
                # 新增新的房屋 ID 到資料庫
                for job_id in ids_to_add:
                    Job.objects.get_or_create(job_id=job_id)
                    
                if ids_to_add.size > 0:
                    jobs_spider.send_telegram(
                        ids_to_add, 
                        'https://www.chickpt.com.tw/job-{}',
                        TOKEN,
                        5298494709 
                    )

                time.sleep(3000)
        # 啟動一個背景執行緒來執行爬蟲任務
        
        threading.Thread(target=run_House591Spider, daemon=True).start()
        threading.Thread(target=run_JobsSpider, daemon=True).start()
    
    def create_SuperUser(self):
        import os
        username = os.getenv("USERNMAE")
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            print('超級使用者已存在')
        else:
            print("開始建立超級使用者")
            User.objects.create_superuser(username=username, email=email, password=password)
            print("已經建立完成")
       

        