# Applying LDA to math.stackexchange.com Data

## Overview
This is part of a larger work in progress of extracting and ranking problems from math.stackexchange.com for use as practice problems for students. You can find all of the posts [here](https://archive.org/download/stackexchange/) in the form of xml files. In this project I take the text from these posts, tokenize them, and use LDA to split these posts into different topics. I do this recursively to build a tree-like organization of the topics. I tried using hierarchical LDA, but it was slower and didn't seem to give me better results.

## Setup
1. Extract https://archive.org/download/stackexchange/mathematica.stackexchange.com.7z to `./xml`.

2. Run `bash setup.sh` to produce a data folder that contains 1) mse.db, a database with the posts and their topics, and 2) topic_descriptions.json, a json file with descriptions of the topics.

3. You can change the number of topics, number of levels, and number of LDA training iterations in `scripts/train.sh`.

## Example
Below is the result of topic splitting with depth three and four topics per level. As you can see, the first two of the four major topics broadly cover elementary mathematics (problem solving and definitions) while the next two cover what might categorized as "numbers" and "abstract structures", mirroring the first two topics, but for advanced mathematics.

```
time problem math book question                             # problem solving
	answer question wine number ball
		puzzle deal box question way
		problem number guess linear integer
		error question sequel yes answer
		wine ball bit poisoned servant
	math book mathematics mathematical theory
		http function well utility www
		math book mathematics problem mathematical
		calculus course theory geometry section
		use history calculator python this
	probability step number time random
		number sequence tour knight binary
		probability day state random time
		people handed handedness study age
		step probability return walk pixel
	time problem value number solution
		time speed calculus problem change
		value time card year chance
		problem solution stamp mathrm number
		game prisoner loses chicken win
frac function point sum line                                # definitions
	function series continuous tiling number
		function distribution fourier mean want
		tiling number sin time way
		function continuous differentiable value limit
		series convergence taylor term frac
	sin circle point triangle angle
		line transformation triangle image circle
		point length line frac segment
		sin triangle cosine angle definition
		square tangent circle vector side
	frac cdot sum sqrt area
		frac sqrt formula mathrm value
		frac sum term cdot cdots
		cdot volume frac cone vec
		theta frac area circle sin
	equation point time value variable
		point equation degree coordinate line
		velocity sin position variable random
		frac curve calculus you way
		integral frac area alpha function
number set real proof prime                                 # numbers
	set proof logic theorem theory
		true formula statement phi gamma
		proof axiom contradiction theory mathematics
		set open closed point finite
		proof order logic sentence semantics
	number set real natural real_number
		set countable size infinity item
		number complex real complex_number negative
		lesson number http org wikipedia
		number natural real set real_number
	real function complex ldots property
		it_s theorem ldots example like
		number rational point rotation scaling
		number riemann zeta function prime
		function real complex number set
	prime number frac root sum
		root polynomial equation solution coefficient
		prime number theorem integer class
		cycle problem element set number
		frac number sum set omega
vector space group matrix product                           # abstract structures
	relation ring category symmetric transitive
		relation transitive symmetric reflexive asymmetric
		ring group homomorphism type element
		equiv sheaf phi pmod module
		category monoidal object relation action
	point lambda function ideal set
		set function operatorname map fractal
		lambda partial constraint lagrange function
		point ideal closed field prime
		log scale line strictly local
	group algebra theory curve representation
		hartshorne space book note geometry
		group algebra theory representation lie
		class chain method field group
		curve elliptic point algebraic example
	vector matrix space product linear
		matrix linear transformation determinant volume
		dual space lambda tensor time
		rotation matrix axis angle quaternion
		vector product space dot cross

```