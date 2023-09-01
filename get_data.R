# This script describes step by step how the JSON can be filtered and
# relevant information, such as the download URL of a distribution, can be extracted.
library(jsonlite)
library(dplyr)

# Access url for the json file with all records from the data catalogue
url="https://www.web.statistik.zh.ch/ogd/daten/zhweb.json"

# Retrieve the json file and convert it into a data frame
data <- jsonlite::fromJSON(url, simplifyDataFrame = T) %>%
  as.data.frame

# Extract all datasets from the municipality portrait
# Identifier is the dataset landinpage
gpzh_only <- data %>%
  dplyr::filter(`dataset.landingPage` == "https://www.zh.ch/de/politik-staat/gemeinden/gemeindeportraet.html")

# Find the record information from the json file (title, description, etc.)
dataset_data <- gpzh_only %>%
  tidyr::unnest(dataset.theme) %>%
  dplyr::select(title = dataset.title,
                description = dataset.description,
                theme = dataset.theme,
                start_date = dataset.startDate,
                end_date =dataset.endDate
                ) %>%
  # Manual correction, as two records deviate from the logic of the other records when naming dataset and resource title.
  dplyr::mutate(title = dplyr::case_when(title == "Anteil Gemeinnützige Wohnungen in Gemeinden des Kantons Zürich [%]" ~ "Anteil Gemeinnützige Wohnungen [%]",
                                         title == "Gemeinnützige Wohnungen in Gemeinden des Kantons Zürich [Anz.]" ~ 	"Gemeinnützige Wohnungen [Anz.]",
                                         TRUE ~ title))

# Retrieve further information on the distribution stored on the second level of the nested json
distibution_data <- as.data.frame(do.call(rbind, gpzh_only$dataset.distribution)) %>%
  dplyr::select("id" = ktzhDistId,
                title,
                "download_url" = downloadUrl,
                format)

# Merging the dataset information with the additional distribution information
gpzh_full_list <- dataset_data %>%
  dplyr::left_join(distibution_data, by = "title") %>%
  dplyr::relocate(c(id, theme), .before = "title")

# Save the full list to a CSV file
utils::write.csv(gpzh_full_list, file = "output/gpzh_dataset_overview.csv", fileEncoding = "UTF-8", row.names = FALSE)
