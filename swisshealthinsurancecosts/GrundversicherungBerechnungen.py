import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Kostenoptimierung der SWICA Versicherungen, Stand 06.03.2022

class realkosten:
    
    def __init__(self, franchise,fixkosten,selbstbehalt,max_arztkosten):
        #make sure that fixkosten and franchise are sorted correctly. 
        #Franchise descending and fixkosten ascending.
        franchise.sort(reverse=True)
        fixkosten.sort()
        
        self.franchise = franchise
        self.selbstbehalt = selbstbehalt
        self.fixkosten = [i * 12. for i in fixkosten]
        self.arztkosten = range(0,max_arztkosten,100)
    
    def kosten_nach_franchise(self,kosten,fixkosten,franchise):
        return (fixkosten + franchise + (kosten-franchise)*self.selbstbehalt)
    
    def realkosten_per_franchise(self,arztkosten,fixkosten,franchise):
        x = []
        for kosten in arztkosten:
            if kosten <= franchise:
                x.append(fixkosten+kosten)
            else:
                x.append(self.kosten_nach_franchise(kosten,fixkosten,franchise))        
        return x
    
    def kosten_berechnung(self):
        return [self.realkosten_per_franchise(self.arztkosten,i,j) for i,j in zip(self.fixkosten,self.franchise)]
    
    def minimalkosten(self):
        
        return [min(np.array(self.kosten_berechnung())[:,i]) for i in range(len(self.arztkosten))] 
    
    def break_even_point(self):
        
        even = []
        index = []
        for f,kosten in zip(self.franchise,self.fixkosten):
            a = [(k-f)*(1-self.selbstbehalt) for k in self.arztkosten] 
            minimum = min(x for x in a if x >= kosten)
            index.append(a.index(minimum))
        return index
    
    #
    #All functions below are for plotting
    #
    def plot_realkosten(self):
        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=(15,10))
        
        ax.set_xlabel("Arztkosten [Chf]",fontsize=25)
        ax.set_ylabel(" Realkosten [Chf]",fontsize=20)

        break_even_index = self.break_even_point()
        
        for i in range(len(self.franchise)):
            ax.plot(self.arztkosten,self.kosten_berechnung()[i],'o-' ,label=str(self.franchise[i])+" Chf")
            
            ax.plot(self.arztkosten[break_even_index[i]], self.kosten_berechnung()[i][break_even_index[i]],'o',markersize=20.,alpha=0.7 ,label='break even for '+str(self.franchise[i])+" Chf")
        
        if (len(self.franchise)>1):
            ax.plot(self.arztkosten,self.minimalkosten(),label='Minimalkosten',alpha=0.7, linewidth=7., c='pink')
        
        ax.tick_params(axis='both', which='major', labelsize=20)
        ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax.grid(b=True, which='major', color='black', linewidth=1.0)
        ax.grid(b=True, which='minor', color='black', linewidth=0.5)
        
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=20)
        return fig
        
    def plot_realkosten_interactiv(self):
        kosten_df = pd.DataFrame(self.kosten_berechnung()).T
        kosten_df.columns=[str(i) for i in self.franchise]
        
        arztkosten_df = pd.DataFrame(self.arztkosten,columns=['arztkosten'])
        
        break_even_index = self.break_even_point()
        x_bev = [self.arztkosten[break_even_index[i]] for i in range(len(self.franchise))]
        y_bev=[self.kosten_berechnung()[i][break_even_index[i]] for i in range(len(self.franchise))]
                 
        df_breakeven = pd.DataFrame({'x':x_bev,'y':y_bev})
        
        if (len(self.franchise)>1):
            minima_df = pd.DataFrame(self.minimalkosten(),columns=['Minimalkosten'])
            minima_df = pd.concat((arztkosten_df,minima_df),axis=1) 
        
        df = pd.concat((arztkosten_df, kosten_df),axis=1) 
        
        
        
        pd.options.plotting.backend = "plotly"
        fig = px.line(df,x=df.columns[0], y=df.columns[1:],width=1100, height=700,
                      template="plotly_white",labels={'arztkosten':'Arztkosten','value':'Realkosten', 'variable':'Franchise Chf'})
        
        #add the minima line
        fig2 = px.line(minima_df,x=minima_df.columns[0],y=minima_df.columns[1])
        fig2.update_traces(line=dict(width = 7.,color='pink'),opacity=.6)
        
        #add the break even points
        fig_be = px.scatter(df_breakeven,x=df_breakeven['x'],y=df_breakeven['y'])
        fig_be.update_traces(marker=dict(size=15,color='red'),opacity=.5)

        fig3 = go.Figure(data=fig.data + fig2.data+fig_be.data, layout = fig.layout)
        
        return fig3
        
  