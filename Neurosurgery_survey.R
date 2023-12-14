library(dplyr)
library(tidyr)
library(ggplot2)
library(knitr)

#################
# Software Info #
#################
#Built with R version `r getRversion()`, dplyr version `r packageVersion("dplyr")`, tidyr version `r packageVersion("tidyr")`, ggplot2 version `r packageVersion("ggplot2")`.

#############################
# Loading and Cleaning Data #
#############################
#We load the dataset:
df <- read.csv("palliative_neurosurgery_survey.csv")

#Order factors
df <- df %>% mutate(
 Demographics_On_Call = factor(Demographics_On_Call, levels = c( "<3 days a month", "3-5 days a month", "5-10 days a month ", ">10 days a month")),
 Demographics_years_of_practise = factor(Demographics_years_of_practise, levels = c( "<5", "5-10", "10-20", ">20" )),
 Futile_Surgery = factor(Futile_Surgery, levels = c( "Never", "Rarely (once a year)", "Sometimes (2-5 a year)", "Often (>5 a year)" )),
 Burnout = factor(Burnout, levels = c( "NO", "MAYBE", "YES" )),
 Moral_Distress_Experience = factor(Moral_Distress_Experience, levels = c( "Strongly disagree", "Generally disagree", "Generally agree", "Strongly agree" )),
 Leaving_Position = factor(Leaving_Position, levels = c( "No, I have never considered leaving or left a position.", "Yes, I considered leaving but did not leave.", "Yes, I left a position.")),
 Communication_Training_Comfortability = factor( Communication_Training_Comfortability, levels = c( "None at all", "A little", "A moderate amount", "A lot", "A great deal" ) ),
 OLBI_result = factor( OLBI_result, levels = c("Not burned out", "At risk", "Burned out") )
)

#Custom function to print out descriptive statistics:
describe <- function( df, column_names, caption ) {
 df %>%
 as_tibble() %>%
 select( all_of(column_names) ) %>%
 pivot_longer( cols = all_of(column_names) ) %>%
 group_by(name) %>%
 summarize_at(
  .vars = vars(value),
  .funs = list(
   min = min,
   Q1 = ~quantile(., probs = 0.25),
   median = median,
   Q3 = ~quantile(., probs = 0.75),
   max= max,
   mean = ~round(mean(.), digits = 2),
   sd = ~round(sd(.), digits = 2)
  )
 ) %>%
 kable( caption = caption )
}

frequency_table <- function( df, variable ) {
 df %>%
 select_at( variable ) %>%
 group_by_at( variable ) %>%
 count() %>%
 mutate( perc = round( (100 * n )/dim(df)[1], digits = 2) ) %>%
 kable( caption = paste( variable, "Counts" ) )
}

describe_univariate <- function( df, variable ) {
 df %>%
 select( all_of( c(variable, "Moral_Distress_Score") ) ) %>%
 group_by_at(variable) %>%
 summarize_at(
  vars(Moral_Distress_Score),
  .funs = list(
   min = min,
   Q1 = ~quantile(., probs = 0.25),
   median = median,
   Q3 = ~quantile(., probs=0.75),
   max= max,
   mean = ~round(mean(.), digits=2),
   sd = ~round(sd(.), digits=2)
  )
 ) %>%
 arrange( desc( median ) ) %>%
 kable( caption = paste("Moral Distress grouped by", variable ) )
}

plot_univariate <- function( df, variable ) {
 ggplot( df, aes( x = .data[[variable]], y = Moral_Distress_Score) ) +
 geom_violin(trim = FALSE) +
 geom_boxplot( width = 0.1 ) +
 ggtitle( paste( "Moral Distress Score by", variable ) )
}

######################################
# Oldenburg Burnout Inventory (OLBI) #
######################################
describe( df = df, column_names = c("OLBI_mean", "OLBI_D_mean", "OLBI_E_mean"), caption = "OLBI Descriptive Statistics" )

##############################
# Moral Distress Description #
##############################
### Total Score and Subscores
ggplot( df, aes( x = Moral_Distress_Score ) ) +
 geom_histogram( bins = 20 ) +
 ggtitle( "Histogram of Moral_Distress_Score" )

describe(
	df = df,
	column_names = c("Moral_Distress_Score", "Moral_Distress_Score_frequency", "Moral_Distress_Score_intensity"), 
	caption = "Moral Distress Score Descriptive Statistics"
)

### Each Question Frequency
frequency_columns <- c(
	"Moral_Distress_1_frequency",
	"Moral_Distress_2_frequency",
	"Moral_Distress_3_frequency",
	"Moral_Distress_4_frequency",
	"Moral_Distress_5_frequency",
	"Moral_Distress_6_frequency",
	"Moral_Distress_7_frequency",
	"Moral_Distress_8_frequency"
)
describe(
	 df = df,
	 column_names = frequency_columns,
	 caption = "Moral Distress Frequency Questions Descriptive Statistics"
)

#Questions sorted by mean frequency (highest to lowest):
df %>% as_tibble() %>% select( all_of( frequency_columns ) ) %>% pivot_longer( all_of(frequency_columns) ) %>% group_by( name ) %>% summarize( mean = mean(value) ) %>% arrange( desc(mean) ) %>% select( name )

### Each Question Intensity
intensity_columns <- c(
	"Moral_Distress_1_intensity",
	"Moral_Distress_2_intensity",
	"Moral_Distress_3_intensity",
	"Moral_Distress_4_intensity",
	"Moral_Distress_5_intensity",
	"Moral_Distress_6_intensity",
	"Moral_Distress_7_intensity",
	"Moral_Distress_8_intensity"
)
describe(
	 df = df,
	 column_names = intensity_columns,
	 caption = "Moral Distress Intensity Questions Descriptive Statistics"
)

#Questions sorted by mean intensity (highest to lowest):
df %>% as_tibble() %>% select( all_of( intensity_columns ) ) %>% pivot_longer( all_of(intensity_columns) ) %>% group_by( name ) %>% summarize( mean = mean(value) ) %>% arrange( desc(mean) ) %>% select( name )

######################################
# Moral Distress Univariate Analysis #
######################################
### Gender
frequency_table( df, "Demographics_gender" )
describe_univariate( df, "Demographics_gender" )
plot_univariate( df, "Demographics_gender" )
wilcox.test(
	Moral_Distress_Score ~ Demographics_gender,
	data = df %>%
		select( Moral_Distress_Score, Demographics_gender ) %>%
		filter( Demographics_gender != "Decline to answer")
)

### Years of practice
frequency_table( df, "Demographics_years_of_practise" )
describe_univariate( df, "Demographics_years_of_practise" )
plot_univariate( df, "Demographics_years_of_practise" )
kruskal.test(
	Moral_Distress_Score ~ Demographics_years_of_practise,
	data = df %>% filter( Demographics_years_of_practise != "Decline to answer" )
)

### Position
frequency_table( df, "Demographics_position" )
describe_univariate( df, "Demographics_position" )
plot_univariate( df, "Demographics_position" )
wilcox.test(
	Moral_Distress_Score ~ Demographics_position,
	data = df
)

### Trauma Center
frequency_table( df, "Demographics_Trauma_Center" )
describe_univariate( df, "Demographics_Trauma_Center" )
plot_univariate( df, "Demographics_Trauma_Center" )
wilcox.test(
    Moral_Distress_Score ~ Demographics_Trauma_Center,
    data = df %>% filter( Demographics_Trauma_Center != "Decline to answer" )
)

### On Call
frequency_table( df, "Demographics_On_Call" )
describe_univariate( df, "Demographics_On_Call" )
plot_univariate( df, "Demographics_On_Call" )
kruskal.test(
    Moral_Distress_Score ~ Demographics_On_Call,
    data = df %>% filter( Demographics_On_Call != "Decline to answer" )
)

### Futile Surgery Frequency
frequency_table( df, "Futile_Surgery" )
describe_univariate( df, "Futile_Surgery" )
plot_univariate( df, "Futile_Surgery" )
  kruskal.test(
    Moral_Distress_Score ~ Futile_Surgery,
    data = df
  )

### Burnout self-assessment
frequency_table( df, "Burnout" )
describe_univariate( df, "Burnout" )
plot_univariate( df, "Burnout" )
  kruskal.test(
    Moral_Distress_Score ~ Burnout,
    data = df
  )

### Burnout by OLBI 
frequency_table( df, "OLBI_result" )
describe_univariate( df, "OLBI_result" )
plot_univariate( df, "OLBI_result" )
  kruskal.test(
    Moral_Distress_Score ~ OLBI_result,
    data = df
  )

### Experienced moral distress during last year
frequency_table( df, "Moral_Distress_Experience" )
describe_univariate( df, "Moral_Distress_Experience" )
plot_univariate( df, "Moral_Distress_Experience" )
kruskal.test(
	Moral_Distress_Score ~ Moral_Distress_Experience,
	data = df
)

### Leaving a position because of moral distress
frequency_table( df, "Leaving_Position" )
describe_univariate( df, "Leaving_Position" )
plot_univariate( df, "Leaving_Position" )
kruskal.test(
	Moral_Distress_Score ~ Leaving_Position,
	data = df
)

############################################################
# Multivariate Regression Analysis of Moral Distress Score #
############################################################
#Without grouping of categories, OLBI categorical (interpretation).
model <- lm(
   Moral_Distress_Score ~ Demographics_years_of_practise + Trauma_Center + Futile_Surgery + OLBI_result + 1,
   data = df %>% mutate(
	Trauma_Center = ifelse( Demographics_Trauma_Center == 'YES', 'yes', 'no')
   )
)
summary(model)

#With grouping of categories, OLBI categorical (interpretation).
model <- lm(
   Moral_Distress_Score ~ years_of_practise + Trauma_Center + Futile_Surgery + OLBI + 1,
   data = df %>% mutate(
	years_of_practise = ifelse( Demographics_years_of_practise %in% c('<5','5-10'), 'short', 'long'),
	Trauma_Center = ifelse( Demographics_Trauma_Center == 'YES', 'yes', 'no'),
	Futile_Surgery = ifelse( Futile_Surgery %in% c('Never', 'Rarely (once a year)'), 'no', 'yes'),
	OLBI = ifelse( OLBI_result == 'Burned out', 'yes', 'no')
   )
)
summary(model)

#Without grouping of categories, OLBI numerical (score).
model <- lm(
   Moral_Distress_Score ~ Demographics_years_of_practise + Trauma_Center + Futile_Surgery + OLBI_mean + 1,
   data = df %>% mutate(
	Trauma_Center = ifelse( Demographics_Trauma_Center == 'YES', 'yes', 'no')
   )
)
summary(model)

#With grouping of categories, OLBI numerical (score).
model <- lm(
   Moral_Distress_Score ~ years_of_practise + Trauma_Center + Futile_Surgery + OLBI_mean + 1,
   data = df %>% mutate(
	years_of_practise = ifelse( Demographics_years_of_practise %in% c('<5','5-10'), 'short', 'long'),
	Trauma_Center = ifelse( Demographics_Trauma_Center == 'YES', 'yes', 'no'),
	Futile_Surgery = ifelse( Futile_Surgery %in% c('Never', 'Rarely (once a year)'), 'no', 'yes')
   )
)
summary(model)

#With grouping of categories, OLBI numerical (score), PHQ9 added.
model <- lm(
   Moral_Distress_Score ~ years_of_practise + Trauma_Center + Futile_Surgery + OLBI_mean + PHQ9 + 1,
   data = df %>% mutate(
	years_of_practise = ifelse( Demographics_years_of_practise %in% c('<5','5-10'), 'short', 'long'),
	Trauma_Center = ifelse( Demographics_Trauma_Center == 'YES', 'yes', 'no'),
	Futile_Surgery = ifelse( Futile_Surgery %in% c('Never', 'Rarely (once a year)'), 'no', 'yes'),
	OLBI = ifelse( OLBI_result == 'Burned out', 'yes', 'no')
   )
)
summary(model)

##########################
# Communication training #
##########################
#* Communication_Training_1: Did you seek out any communication training to help you with hyperintense communication during you residency?  (YES, NO)
#* Communication_Training_2: Did you receive training specific to lead goal of care communication during your residency?  (YES, NO)
#Communication_Training_3: Did you seek out any communication training to help you with hyperintense communication after you graduated?  (YES, NO)
#* Communication_Training_4: Would you be interested in communication training to help you navigate hyperintense communication? (YES, NO)
#* Communication_Training_Skills: For the following statement, please indicate how much you agree or disagree: I have the necessary skills to discuss end of life goals in neurosurgery patients. (Strongly disagree, Generally disagree, Generally agree, Strongly agree)
df %>%
 select( Communication_Training_1, Communication_Training_2, Communication_Training_3, Communication_Training_4 ) %>%
 pivot_longer(c(Communication_Training_1, Communication_Training_2, Communication_Training_3, Communication_Training_4)) %>%
 table() %>%
 as_tibble() %>%
 pivot_wider(names_from = value, values_from = n) %>%
 mutate( NO_perc = round( (100 * NO)/dim(df)[1], digits = 2), YES_perc = round( (100 * YES)/dim(df)[1], digits = 2) ) %>%
 kable(caption = "Communication Training Summary Statistics")

#Communication_Training_Skills: For the following statement, please indicate how much you agree or disagree: I have the necessary skills to discuss end of life goals in neurosurgery patients.
df %>%
 select( Communication_Training_Skills ) %>%
 table() %>%
 as_tibble() %>%
 mutate( Perc = round( (100 * n) / dim(df)[1], digits = 2) ) %>%
 kable(caption = "Communication Training Skills Summary Statistics")

#Communication_Training_Comfortability: How comfortable do you feel engaging in hyper-intense conversations. Hyper-intense conversations.are defined as situations in which you have to break bad news to a patient or patient’s family member (death, poor prognosis, or withdrawal of life sustaining treatments).
df %>%
 select( Communication_Training_Comfortability ) %>%
 table() %>%
 as_tibble() %>%
 mutate( Perc = round( (100 * n )/dim(df)[1] , digits = 2) ) %>%
 kable( caption = "Communication Training Comfortability" )

###################
# Palliative Care #
###################
#* Palliative_Care_Availability: Is palliative care available as a specialty service at your institution?  (YES, NO)
#* Palliative_Care_TBI: On which patient do you routinely consult palliative care? (check all that apply) Severe TBI (YES, NO)
#* Palliative_Care_GBM: On which patient do you routinely consult palliative care? (check all that apply) Recurrent GBM (YES, NO)
#* Palliative_Care_Metastatic: On which patient do you routinely consult palliative care? (check all that apply) Widely metastatic disease (YES, NO)
#* Palliative_Care_Rarely: On which patient do you routinely consult palliative care? (check all that apply) I rarely consult palliative care (YES, NO)
#* Palliative_Care_Other: On which patient do you routinely consult palliative care? (check all that apply) x Other...  (NO, free text)
#* Palliative_Care_Reason1: What are the reasons you consult palliative care? (check all that apply) Patient likely to die during this admission (YES, NO)
#* Palliative_Care_Reason2: What are the reasons you consult palliative care? (check all that apply) Difficult family dynamics (YES, NO)
#* Palliative_Care_Reason3: What are the reasons you consult palliative care? (check all that apply) End of life discussion is needed (YES, NO)
#* Palliative_Care_Reason4: What are the reasons you consult palliative care? (check all that apply) Patient’s/family’s request (YES, NO)
#* Palliative_Care_Reason5: What are the reasons you consult palliative care? (check all that apply) Time constraints in hyperintense conversations (YES, NO)
#* Palliative_Care_Reason6: What are the reasons you consult palliative care? (check all that apply) Lack of training in having hyperintense conversations (YES, NO)
#* Palliative_Care_Reason7: What are the reasons you consult palliative care? (check all that apply) Other (NO, free text)
df %>%
 select( 
  Palliative_Care_Availability,
  Palliative_Care_TBI,
  Palliative_Care_GBM,
  Palliative_Care_Metastatic,
  Palliative_Care_Rarely,
  Palliative_Care_Reason1,
  Palliative_Care_Reason2,
  Palliative_Care_Reason3,
  Palliative_Care_Reason4,
  Palliative_Care_Reason5,
  Palliative_Care_Reason6
 ) %>%
 pivot_longer( c(
  Palliative_Care_Availability,
  Palliative_Care_TBI,
  Palliative_Care_GBM,
  Palliative_Care_Metastatic,
  Palliative_Care_Rarely,
  Palliative_Care_Reason1,
  Palliative_Care_Reason2,
  Palliative_Care_Reason3,
  Palliative_Care_Reason4,
  Palliative_Care_Reason5,
  Palliative_Care_Reason6
 )) %>%
 table() %>%
 as_tibble() %>%
 pivot_wider(names_from = value, values_from = n) %>%
 mutate( NO_perc = round( (100 * NO)/dim(df)[1], digits = 2), YES_perc = round( (100 * YES)/dim(df)[1], digits = 2) ) %>%
 kable(caption = "Communication Training Summary Statistics")

pal <- df %>%
 select(
  Palliative_Care_Availability,
  Palliative_Care_TBI,
  Palliative_Care_GBM,
  Palliative_Care_Metastatic,
  Palliative_Care_Rarely,
  Palliative_Care_Reason1,
  Palliative_Care_Reason2,
  Palliative_Care_Reason3,
  Palliative_Care_Reason4,
  Palliative_Care_Reason5,
  Palliative_Care_Reason6
 ) %>%
 pivot_longer( c(
  Palliative_Care_Availability,
  Palliative_Care_TBI,
  Palliative_Care_GBM,
  Palliative_Care_Metastatic,
  Palliative_Care_Rarely,
  Palliative_Care_Reason1,
  Palliative_Care_Reason2,
  Palliative_Care_Reason3,
  Palliative_Care_Reason4,
  Palliative_Care_Reason5,
  Palliative_Care_Reason6
 )) %>%
 table() %>%
 as_tibble() %>%
 pivot_wider(names_from = value, values_from = n) %>%
 arrange(name)

ggplot(pal, aes( y = name, x = NO ) ) +
 geom_bar(stat="identity") +
 ggtitle( "Bar plot of Palliative Care Questions." )

#Palliative_Care_Other: On which patient do you routinely consult palliative care? (check all that apply) x Other...  (NO, free text)
df %>% select( Palliative_Care_Other ) %>% table() %>% as_tibble()

#Palliative_Care_Reason7: What are the reasons you consult palliative care? (check all that apply) Other (NO, free text)
df %>% select( Palliative_Care_Reason7 ) %>% table() %>% as_tibble()

##############
# Depression #
##############
describe( df = df, column_names = c("PHQ9"), caption = "PHQ9 Descriptive Statistics" )

ggplot( df, aes( x = PHQ9 ) ) +
 geom_histogram( bins = 15 ) +
 ggtitle( "Histogram of PHQ9" )

### Depression and Moral Distress
#Scatter
ggplot( df, aes( x = Moral_Distress_Score, y = PHQ9 ) ) +
 geom_point() +
 geom_smooth(method = "lm" , formula = "y ~ x") +
 ggtitle( "Scatter plot PHQ9 vs. Moral Distress Score" )

#Pearson's correlation coefficient of Moral Distress Score and PHQ9:
cor.test(df$PHQ9, df$Moral_Distress_Score)

#Linear regression model of Moral Distress Score and PHQ9:
model <- lm ( PHQ9 ~ Moral_Distress_Score, df)
summary(model)

### Depression and Burnout
ggplot( df, aes( x = OLBI_mean, y = PHQ9 ) ) +
 geom_point() +
 geom_smooth(method = "lm" , formula = "y ~ x") +
 ggtitle( "Scatter plot PHQ9 vs. Oldenburg Burnout Inventory" )

#Pearson's correlation coefficient of Burnout and PHQ9:
cor.test(df$PHQ9, df$OLBI_mean)

#Linear regression model of OLBI and PHQ9:
model <- lm ( PHQ9 ~ OLBI_mean, df)
summary(model)

#Self-reported Burnout:
kruskal.test(
	PHQ9 ~ Burnout,
	data = df
)

ggplot( df, aes( x = Burnout, y = PHQ9 ) ) +
 geom_violin(trim = FALSE) +
 geom_boxplot( width = 0.1 ) +
 ggtitle( "PHQ9 by self-reported Burnout" )

### Depression Multivariate Regression Analysis
model <- lm ( PHQ9 ~ Moral_Distress_Score + OLBI_mean, df)
summary(model)

ggplot( df, aes( x = Moral_Distress_Score, y = OLBI_mean, size = PHQ9 ) ) +
 geom_point() +
 ggtitle("PHQ9 predicted by Moral_Distress_Score and OLBI")
