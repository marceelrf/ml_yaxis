
	options(warn=-1)
	list.of.packages <- c('ggplot2','plotly','htmlwidgets','stringr')
	new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,'Package'])]
	if(length(new.packages)) install.packages(new.packages)

	library(ggplot2)
	library(plotly)
	library(htmlwidgets)
	library(stringr)

	setwd('/media/lab/Data/kir-mapper_SABE/output//ncopy//plots/')
	db <- read.table('5UPKIR_plot_db.txt',h=T,sep='\t')

	onecp = 0.300000 
	twocp = 0.700000 
	threecp = 1.500000
	fourcp = 2.000000


	count <- length(unique(db$Sample))

	p <- ggplot(data=db) + 
		geom_point(aes(x=Order,y=Ratio,group=Sample,color=Heterozygosis),size=1) + 
		theme_minimal() + 
		xlab('') +
		ylab('5UPKIR / KIR3DL3 ratio') +
		theme(
				axis.text.x = element_blank(),
				axis.ticks = element_blank(),
			legend.title = element_text(size = 8),
			legend.text = element_text(size = 6),
			plot.caption = element_text(size = 6)) +
		geom_hline(aes(yintercept=onecp, linetype = '0-1 copy threshold'),colour='red') + 
		geom_hline(aes(yintercept=twocp, linetype = '1-2 copy threshold'),colour='blue') + 
		geom_hline(aes(yintercept=threecp, linetype = '2-3 copy threshold'),colour='orange') + 
		geom_hline(aes(yintercept=fourcp, linetype = '3-4 copy threshold'),colour='green') + 
		scale_linetype_manual(name = 'Thresholds', values = c(2, 2, 2, 2), 
			guide = guide_legend(override.aes = list(color = c('red', 'blue', 'orange', 'green')))) +
		labs(title='5UPKIR', caption = 'Calculated using the wgs mode')
	
	ggsave("/media/lab/Data/kir-mapper_SABE/output//ncopy//plots//5UPKIR.png", width=8, height=6,bg = "white")
	
	myplot <- ggplotly(p)
	
	myplot <- ggplotly( p ) %>%
	  layout( legend=FALSE )
	
		for (i in 1:length(myplot$x$data)){
	  if (!is.null(myplot$x$data[[i]]$name)){
	    myplot$x$data[[i]]$name =  gsub("\\(","",str_split(myplot$x$data[[i]]$name,",")[[1]][1])
	  }
	}
	
	saveWidget(myplot, '/media/lab/Data/kir-mapper_SABE/output//ncopy//plots//5UPKIR.html', selfcontained = F, libdir = '/media/lab/Data/kir-mapper_SABE/output//ncopy//plots//5UPKIR')