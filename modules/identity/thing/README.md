# Thing
A subject or an object that one need not, cannot, or does not wish to give a specific name to.

## Subject and object (philosophy)

In philosophy, a subject is a being that exercises agency, undergoes conscious experiences, and is situated in relation to other things that exist outside itself; thus, a subject is any individual, person, or observer. An object is any of the things observed or experienced by a subject, which may even include other beings (thus, from their own points of view: other subjects).

A simple common differentiation for [subject and object]((https://en.wikipedia.org/wiki/Subject_and_object_(philosophy))) is: an observer versus a thing that is observed. In certain cases involving personhood, subjects and objects can be considered interchangeable where each label is applied only from one or the other point of view. Subjects and objects are related to the philosophical distinction between subjectivity and objectivity: the existence of knowledge, ideas, or information either dependent upon a subject (subjectivity) or independent from any subject (objectivity).

## Device

a thing made or adapted for a particular purpose.

## Quiddity

In scholastic philosophy, ["quiddity"](https://en.wikipedia.org/wiki/Quiddity) (/ˈkwɪdɪti/; Latin: quidditas) was another term for the essence of an object, literally its "whatness" or "what it is".   
Quiddity is the essence that makes something the kind of thing it is and makes it different from any other

Quiddity describes properties that a particular substance (e.g. a person) shares with others of its kind. The question "what (quid) is it?" asks for a general description by way of commonality. This is quiddity or "whatness" (i.e., its "what it is"). Quiddity was often contrasted by the scholastic philosophers with the haecceity or "thisness" of an item, which was supposed to be a positive characteristic of an individual that caused it to be this individual, and no other. It is used in this sense in British poet George Herbert's poem, "Quiddity". Example: What is a "tree"? We can only see specific trees in the world around us - the category "tree" which includes all trees is a classification in our minds, not empirical, and not observable. The quiddity of a tree is the collection of characteristics which make it a tree. This is sometimes referred to as "treeness". This idea fell into disuse with the rise of empiricism, precisely because the essence of things, that which makes them what they are, does not correspond to any observables in the world around us. Nor can it be logically arrived at.

### Definition
- That which gives anything its specific uniqueness; essential nature.
- Essential nature of a thing
- Trivial point of contention

## Animate and Inanimate

We categorize things in two categories **Animate** and **Inanimate**. Animates will introduce in `user` and its subdomains as `organization`, `person`, ... domain and Inanimate e.g. `estate`, ...

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### User-assigned object labels - edges/user-relation-object.go
- **Idea**: when users assign certain labels to their objects, they allow others to get and see them (candidates: UserPicture, UserPrimaryPicture); a user preference can limit access to some relation level (e.g. only the 1stFriendshipCycle); rules CAN limit users from using these labels for external reasons (e.g. governments forcing a clear face in pictures).
- **Review questions**: is label-driven access an authorization rule evaluation over the social graph (rights domain), or a property of the label edge? This is the clearest meeting point of identity, social connections, and rights.

### Picture rating - edges/picture/obejct.go
- **Idea**: PictureRating scale 0-3: 0 = suitable for all websites/audiences; 1 = rude gestures, provocatively dressed individuals, mild swearing, mild violence; 2 = harsh profanity, intense violence, nudity, hard drug use; 3 = hardcore sexual imagery or extremely disturbing violence.
- **Review questions**: does content rating belong to knowledge/content instead of thing? Is the 4-level scale one vocabulary or per-jurisdiction policy?

### Currency labels - edges/count_unit/labels/currency/edges/currency.go
- **Idea**: currency as a count-unit label with DecimalNumber (e.g. 8099 >> 80.99) and a settlement-reference Domain field (mediatype precedent referenced).
- **Review questions**: does decimal placement belong to the count unit or to the money module (economics)?

### Criterion (data model; idea semantics only)
- **Idea**: task evaluation criteria with a generic Point (percent, star, ...); story-point estimation (Atlassian) referenced as precedent.
- **Review questions**: is criterion a task-side edge (management) rather than thing-side?