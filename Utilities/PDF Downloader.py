import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import re

# Function to get search results with pagination
def get_search_results(query, num_pages=3):
    pdf_links = []
    for page in range(num_pages):
        # Calculate start parameter for Google pagination (10 results per page)
        start = page * 10
        base_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&start={start}"
        
        # Send a GET request to the search URL
        response = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"})
        
        # Check if the request was successful
        if response.status_code == 200:
            pdf_links += extract_pdf_links(response.text)
        else:
            print(f"Failed to retrieve search results from page {page + 1}.")
            break
    
    return pdf_links

# Function to parse search results and extract valid PDF links
def extract_pdf_links(html_content):
    pdf_links = []
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all anchor tags
    for link in soup.find_all('a'):
        href = link.get('href')
        
        # Check if the href is a valid .pdf link and not a Google search-related URL
        if href and ".pdf" in href and "url?q=" in href:
            # Clean up the URL
            clean_link = href.split("&")[0]
            clean_link = clean_link.replace("/url?q=", "")
            
            # Ensure the link has a proper scheme and is a valid PDF URL
            if clean_link.startswith("http") and clean_link.endswith(".pdf"):
                pdf_links.append(clean_link)
    
    return pdf_links

# Function to download PDFs
def download_pdfs(pdf_links, download_dir="pdfs"):
    # Create directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    for pdf_link in pdf_links:
        # Get the PDF file name
        pdf_name = pdf_link.split("/")[-1]
        pdf_path = os.path.join(download_dir, pdf_name)
        
        # Download the PDF
        try:
            response = requests.get(pdf_link, timeout=10)
            response.raise_for_status()  # Ensure we catch HTTP errors
            with open(pdf_path, 'wb') as file:
                file.write(response.content)
                print(f"Downloaded: {pdf_name}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {pdf_link}: {e}")

# Main function to run the program
def main():
    query = input("Enter the search keywords: ")
    num_pages = int(input("Enter the number of pages to search: "))
    
    pdf_links = get_search_results(query, num_pages)
    
    if pdf_links:
        print(f"Found {len(pdf_links)} PDF files.")
        download_pdfs(pdf_links)
    else:
        print("No valid PDF links found.")

# Run the program
if __name__ == "__main__":
    main()
