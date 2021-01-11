# Author: Oana Florean
# R version 4.0.0 (2020-04-24)

library(jsonlite)

args <- commandArgs(trailingOnly = TRUE)

search_type <- args[1] 
search_value <- args[2]

if (search_type == "-t") {
  url <- paste("https://platform-api.opentargets.io/v3/platform/public/association/filter?target=", search_value, "&size=10000&fields=target.id&fields=disease.id&fields=association_score.overall", sep="")
  
}

if (search_type == "-d") {
  url <- paste("https://platform-api.opentargets.io/v3/platform/public/association/filter?disease=", search_value, "&size=10000&fields=target.id&fields=disease.id&fields=association_score.overall", sep="")
  
}

req <- fromJSON(url, flatten = TRUE)
data <- req$data
data
print(paste0("Min: ",min(data$association_score.overall)))
print(paste0("Max: ",max(data$association_score.overall))) 
print(paste0("Average: ",mean(data$association_score.overall)))
print(paste0("Standard Deviation: ",sd(data$association_score.overall)))

# Instruction example to run in command prompt:
# "C:\..\Rscript.exe" "C:\..\target.R" -t ENSG00000197386



