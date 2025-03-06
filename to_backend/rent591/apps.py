from django.apps import AppConfig



from .爬蟲 import House591Spider

class Rent591Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rent591'
    def ready(self):
        import threading , time
        from .models import House
        def run_spider():
            spider = House591Spider()
            filter_params = [
                {
                "region":"3",
                "kind":"2",
                "price":"0_5000,5000_10000",
                "notice" : "all_sex"
                },
                {
                "region":"3",
                "kind":"3",
                "price":"0_5000,5000_10000",
                "notice" : "all_sex"
                }
                ]
            sort_params = {
                'sort': 'money_desc'  # 租金由高到低排序
            }

            filter_params_index=len(filter_params)
            
            while True:
                
                filter_params_index= filter_params_index- 1 if filter_params_index > 0 else len(filter_params)-1
                
                new_house_ids = spider.search(filter_params[filter_params_index], sort_params)
                
                # 獲取資料庫中的所有房屋 ID
                old_house_ids = set(House.objects.values_list('house_id', flat=True))

                # # 找出需要刪除的房屋 ID
                # ids_to_delete = old_house_ids - new_house_ids
                # House.objects.filter(house_id__in=ids_to_delete).delete()
                
                # 找出需要新增的房屋 ID
                ids_to_add = new_house_ids - old_house_ids
                
                # 新增新的房屋 ID 到資料庫
                for house_id in ids_to_add:
                    House.objects.create(house_id=house_id)
                    
                if ids_to_add:
                    spider.sendTele(ids_to_add)
                    
                time.sleep(300)
        # 啟動一個背景執行緒來執行爬蟲任務
        threading.Thread(target=run_spider, daemon=True).start()