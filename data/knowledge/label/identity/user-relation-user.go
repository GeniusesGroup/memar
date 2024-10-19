/* For license and copyright information please see the LEGAL file in the code repository */

package label

// https://kottke.org/21/06/the-circles-of-friendship
const (
	// The innermost layer of 1.5 is [the most intimate]; clearly that has to do with your romantic relationships.
	RelationType_1stFriendshipCycle = iota // Ego, Usually < 2

	// The next layer of five is your shoulders-to-cry-on friendships.
	// They are the ones who will drop everything to support us when our world falls apart.
	RelationType_2stFriendshipCycle // Close Friends. Usually < 5

	// The 15 layer includes the previous five, and your core social partners.
	// They are our main social companions, so they provide the context for having fun times.
	// They also provide the main circle for exchange of child care.
	// We trust them enough to leave our children with them.
	RelationType_3stFriendshipCycle // Best Friends. Usually < 15

	// The next layer up, at 50, is your big-weekend-barbecue people.
	RelationType_4stFriendshipCycle // Good Friends. Usually < 50

	// And the 150 layer is your weddings and funerals group who would come to your once-in-a-lifetime event.
	RelationType_5stFriendshipCycle // Friends. Usually < 150

	// a relationship less intimate than friendship
	RelationType_Acquaintances // Usually < 500

	RelationType_KnownNames // Usually < 1500

	RelationType_KnownFaces // Usually < 5000

	// Usually use to make or start to making friendship.
	RelationType_Follow
)
