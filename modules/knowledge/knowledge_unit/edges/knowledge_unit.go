/* For license and copyright information please see the LEGAL file in the code repository */

package label

// education unit type
// ?? > science > field > course > lessons > topics > ??
const (
	// the state of knowing : knowledge as distinguished from ignorance or misunderstanding
	Type_Science = iota

	// a branch of knowledge
	Type_Field

	// education imparted in a series of lessons or meetings
	Course

	Type_Lesson
	Type_Topic
)
