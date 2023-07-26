/* For license and copyright information please see the LEGAL file in the code repository */

package urup

type User_Relation uint8

// https://kottke.org/21/06/the-circles-of-friendship
const (
	User_Relation_Unset User_Relation = iota

	// The innermost layer of 1.5 is [the most intimate]; clearly that has to do with your romantic relationships.
	User_Relation_1stFriendshipCycle // Ego, Usually < 2

	// The next layer of five is your shoulders-to-cry-on friendships.
	// They are the ones who will drop everything to support us when our world falls apart.
	User_Relation_2stFriendshipCycle // Close Friends. Usually < 5

	// The 15 layer includes the previous five, and your core social partners.
	// They are our main social companions, so they provide the context for having fun times.
	// They also provide the main circle for exchange of child care.
	// We trust them enough to leave our children with them.
	User_Relation_3stFriendshipCycle // Best Friends. Usually < 15

	// The next layer up, at 50, is your big-weekend-barbecue people.
	User_Relation_4stFriendshipCycle // Good Friends. Usually < 50

	// And the 150 layer is your weddings and funerals group who would come to your once-in-a-lifetime event.
	User_Relation_5stFriendshipCycle // Friends. Usually < 150

	// a relationship less intimate than friendship
	User_Relation_Acquaintances // Usually < 500

	User_Relation_KnownNames // Usually < 1500

	User_Relation_KnownFaces // Usually < 5000

	// Usually use to make or start to making friendship.
	User_Relation_Follow
)
