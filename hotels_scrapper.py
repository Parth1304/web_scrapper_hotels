from playwright.sync_api import sync_playwright
import pandas as pd

def main():
    with sync_playwright() as p:
        checkin_date = '2024-07-20'
        checkout_date = '2024-07-23'
        
        page_url = f'https://www.booking.com/searchresults.en-gb.html?label=en-in-booking-desktop-SoQWfYhAMBURf0HSQntj1AS652796016141%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-334108349%3Alp9144438%3Ali%3Adec%3Adm&gclid=Cj0KCQjwj9-zBhDyARIsAERjds1EIMwSpCCP1TmtWmBq7mz3C5ZU9cCfz-Cz5UPPpZqYjnqgH_jMXTEaAqI_EALw_wcB&aid=2311236&checkin={checkin_date}&checkout={checkout_date}&dest_id=-2103603&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null'
        
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
        
        hotels_list = []

        while True:
            # Wait for hotel cards to load
            page.wait_for_selector('//div[@data-testid="property-card"]')
            
            # Get all hotel cards on the current page
            hotels = page.locator('//div[@data-testid="property-card"]').all()
            print(f'There are {len(hotels)} hotels on the current page.')
            
            for hotel in hotels:
                hotel_dict = {}
                hotel_dict['name'] = hotel.locator('//div[@data-testid="title"]').inner_text()
                
                price_text = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
                hotel_dict['price'] = price_text  # Directly use the extracted text
                
                hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
                hotel_dict['Avg reviews'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
                hotel_dict['Reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

                hotels_list.append(hotel_dict)

            # Check if the "Load More" button is present
            load_more_button = page.locator('//button[contains(@class, "bf33709ee1") and contains(@class, "a190bb5f27") and contains(@class, "b9d0a689f2") and contains(@class, "bb5314095f") and contains(@class, "b81c794d25") and contains(@class, "da4da790cd") and span[text()="Load more results"]]')
            if load_more_button.is_visible():
                load_more_button.click()
                page.wait_for_timeout(5000)  # Wait for the new results to load
            else:
                break
        
        # Create a DataFrame and save it to a CSV and Excel file
        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False)
        df.to_csv('hotels_list.csv', index=False, encoding='utf-8')  # Ensure the CSV is saved with UTF-8 encoding
        
        browser.close()

if __name__ == '__main__':
    main()
 