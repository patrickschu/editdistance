# -*- coding: utf-8 -*-

vars = ["e/0","y/i","u/v","0/e","ie/y","ll/l","th/s","v/u","eth/s","'/e","e/ee","0/a","i/j","u/0","i/y","~/n","ee/e","e/i","nn/n","k/0","l/ll","o/u","re/er","o/oo","y=/th","e/a","s/ss","0/u","i/0","i/e","tt/t","y/0","chir/s","e/o","t/tt","a/0","y=/i","0/i","a/e","th/es","oo/o","0/h","t/c","u/o","~/m","vv/w","o/a","n/nn","c/t","mm/m","ke/0","d/0","ke/c","yu/iv","c/s","h/0","pp/p","y/e","0/w","a/o","re/ar","t/ed","s/c","rr/r","dd/d","p/pp","v/f","0/o","e/'","f/ph","ke/ch","s/0","te/at","u~/n","w/u","'/i","æ/e","c/0","d/dd","ey/ai","gg/g","t/0","th/ds","bb/b","ie/eo","r/rr","th/d","ye/i","yke/ic","yke/ick","0/c","0/d","0/s","ay/ei","de/ad","i/ii","j/0","o/0","r/0","ss/s","u/av","uy/vi","w/g","0/icl","0/n","*=/h","*=/i","e/y","k/ch","m/mm","o/e","p/0","the/s","y~/it","'/ugh","0/t","0/ugh","~/ith","ai/e","ake/uck","at/0","chyr/s","e/u","ea/ie","ee/y","eh/s","es/0","est/0","eu/iv","ff/f","ll/nce","n/0","te/a","th/ps","the/es","tteth/t","u/w","y/o","0/b","0/g","~/n'","a/be","el/le","eth/0","h/s","ia/eo","ie/eon","me/am","n/m","n/u","on/ng","r/m","reth/ars","s/r","st/0","th/rs","u/iv","we/u","x/c","y'/ie","yd/eth","*-/e_","'t/ed","0/de","0/m","0/te","*=/o","a/aa","a/i","am/me","an/oo","ar/re","æ/ae","be/n","cy/ti","e/ai","e/ia","e/s","ea/i","ei/ie","ecke/ick","en/0","euy/igh","ew/u","ey/0","f/ff","fe/ef","fer/0","g/gg","i/ee","ie/yi","k/h","ke/ak","ke/h","keth/aks","m/0","ne/an","ne/gn","on/um","que/c","s/ce","s/z","t/s","ta/0","th/ms","th/ns","u/ew","u/n","ure/wer","v/eu","w/0","w/ugh"]

vars = [i.split("/") for i in vars]


for var in vars:
	if len(var) != 2:
		print "ALARM ", var
	cmd = " ".join(
	["python variantfinder.py", 
	var[0], 
	var[1], 
	"--read_corpusfile vocab.json",
	 "--output_position",
	  "".join(
	  ["marcos_csvs/",
	  var[0], 
	  "_", 
	  var[1],
	  "_0715_spreadsheet"])])
	print cmd

