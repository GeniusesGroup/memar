/* For license and copyright information please see the LEGAL file in the code repository */

package ekup

// education unit type
type Type uint32

// ?? > science > field > course > lessons > topics > ??
const (
	Type_Unset Type = 0

	// the state of knowing : knowledge as distinguished from ignorance or misunderstanding
	Type_Science Type = iota

	// a branch of knowledge
	Type_Field

	// education imparted in a series of lessons or meetings
	Type_Course

	Type_Lesson
	Type_Topic
)
