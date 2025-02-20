import logging
import random

from datetime import datetime

logger = logging.getLogger(__name__)


class CommonServiceImpl:

    # process the work order id
    def generate_unique_id(self,table,field,type):
        
        while True:
            current_datetime = datetime.now()
            # getting year and month as first 4 digits
            date_part = f"{current_datetime.year % 100:02d}{current_datetime.month:02d}"
            # 4 digits from time in milliseconds
            time_part = f"{current_datetime.microsecond // 1000:04d}"
            # 2 digits as random
            random_part = f"{random.randint(0, 99):02d}"
            # appending the above together
            generated_id = type + str(date_part + time_part + random_part)
            print("ID ",generated_id)
            if not self.check_id(generated_id,table,field):
                return generated_id
    
    # id check process
    def check_id(self,gen_id,table,field):
        check_id = table.objects.filter(**{field: gen_id}).exists()
        if check_id:
            return True