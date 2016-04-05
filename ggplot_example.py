## Source: http://www.r-bloggers.com/ggplot2-in-python-a-major-barrier-broken/
import numpy as np
import pandas as pd
import rpy2.robjects as robj
import rpy2.robjects.pandas2ri # for dataframe conversion
from rpy2.robjects.packages import importr

## First, make some random data
x = np.random.normal(loc = 5, scale = 2, size = 10)
y = x + np.random.normal(loc = 0, scale = 2, size = 10)

## Transform the data to a pandas dataframe.
testData = pd.DataFrame( {'x':x, 'y':y} )

## Make an R-object containing function that makes the plot.
plotFunc = robj.r("""
library(ggplot2)

function(df){
      p <- ggplot(df, aes(x, y)) + geom_point()
      print(p)
      }
""")

## Import graphics devices.
gr = importr('grDevices')

## Convert the testData to an R dataframe
robj.pandas2ri.activate()
testData_R = robj.conversion.py2ri(testData)

## Run the plot function on the dataframe
plotFunc(testData_R)

## This requires you to press enter, otherwise the plot window closes
raw_input()

## Shut down the window using dev_off()
gr.dev_off()

## Save the output in a pdf
plotFunc_2 = robj.r("""
library(ggplot2)

function(df){
      p <- ggplot(df, aes(x, y)) + geom_point( ) +
            theme(panel.background = element_rect(fill = NA, color = 'black'))
      ggsave('rpy2_magic.pdf', plot = p, width = 6.5, height = 5.5)
      }
""")

## Modify and run the function again with saving the file
plotFunc_2(testData_R)
