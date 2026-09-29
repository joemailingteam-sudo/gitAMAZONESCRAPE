# Amazon  Product Scraper

A Python-based web scraper for collecting product information from **Amazon Egypt (Amazon)** using Playwright and an Oxylabs Web Unblocker proxy.

## Overview

This project is designed to scrape product search results from Amazon  based on a specified search query.

For example, the current script searches for:

**Pressure Cooker**

The scraper can collect product information across multiple search-result pages and save the results in a structured file.

## Data Collected

For each product, the scraper collects:

* **Product Title**
* **Price**
* **Rating**
* **Product Link**

## Output Formats

The scraped data can be saved as:

* **CSV**
* **JSON**

The default output is a CSV file.

Example:

`pressure cooker_product.csv`

## Amazon Website

The scraper targets:

**Amazon Egypt — https://www.amazon.com**

## Proxy Support

The project uses **Oxylabs Web Unblocker** to provide proxy access when making requests to Amazon Egypt.

It also checks the proxy connection and saves the returned response to:

`result.html`

## Pagination

The scraper supports scraping multiple Amazon search-result pages.

The current configuration is set to scrape:

**2 pages**

The number of pages can be changed according to the intended scraping task.

## CAPTCHA Detection

The scraper includes detection for Amazon CAPTCHA/block pages.

If a CAPTCHA is detected, the scraping process stops instead of continuing to collect invalid results.

## Example Search

The current script is configured for:

`pressure cooker`

It produces a file containing the collected product information, such as:

| Title        | Price | Rating | Link               |
| ------------ | ----- | ------ | ------------------ |
| Product name | Price | Rating | Amazon product URL |

## Technologies

* Python
* Playwright
* Requests
* Oxylabs Web Unblocker
* CSV
* JSON

## Project Purpose

The main purpose of this project is to **automatically collect Amazon Egypt product search data into structured files**, making the data easier to analyze, organize, or use in other applications.
