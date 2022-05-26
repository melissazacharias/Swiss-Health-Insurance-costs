import streamlit as st
import GrundversicherungBerechnungen as gk
import re


st.title('Grundversicherung')

#franchise = [2500.,2000.,1500.,1000.,500.,300.]

selbstbehalt = st.number_input(label='Selbstbehalt in %:',value=10)

#fixkosten = [300.,311.0,335.60,361.50,386.20,397.00]# fixkosten nach Franchise

selbstbehalt = selbstbehalt/100.

collect_numbers = lambda x : [int(i) for i in re.split("[^0-9]", x) if i != ""]

st.write('Bitte Franchisen als Kommagetrennte Liste angeben. Z.B: 300,500,2000')
franchise = st.text_input("Franchisen in Chf:",value='2500,2000,1500,1000,500,300' )
franchise = collect_numbers(franchise)
#st.write(franchise, type(franchise[0]))

st.write('Bitte Prämien als Kommagetrennte Liste angeben. Z.B: 300,500,2000')
fixkosten = st.text_input("Prämien in Chf:", value='300,311,335,361,386,397')
fixkosten = collect_numbers(fixkosten)
#st.write(fixkosten)

arztkosten_max = 7000
arztkosten = range(0,arztkosten_max,100)

x = gk.realkosten(franchise,fixkosten,selbstbehalt,arztkosten_max)


#st.write(x.plot_realkosten())

st.plotly_chart(x.plot_realkosten_interactiv(), use_container_width=False)