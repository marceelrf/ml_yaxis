library(tidyverse)


files_sabe <- list.files(path = 'SABE/ncopy/plots/',
                        pattern = 'plot_db.txt',
                        full.names = TRUE)
files_sabe

file_name <- stringr::str_replace(files_sabe,'SABE/ncopy/plots//',"")
file_name <- stringr::str_replace(file_name,'_plot_db.txt',"")
file_name

sabe_dbs <- purrr::map(files_sabe,read_tsv) 

sabe_dbs[[1]]
names(sabe_dbs) <- file_name

# Plots

sabe_dbs$KIR2DL2 %>%
    ggplot(aes(x = Ratio)) +
    geom_density(fill = "dodgerblue")


sabe_dbs$KIR2DL2 %>%
    ggplot(aes(x = Ratio,fill = Gene)) +
    geom_density(alpha = .5)

sabe_dbs$KIR2DL2 %>%
    ggplot(aes(x = Ratio,fill = Gene)) +
    geom_density(alpha = .5) +
    facet_wrap(~Heterozygosis,nrow = 3)
