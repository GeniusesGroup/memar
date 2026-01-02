/* For license and copyright information please see the LEGAL file in the code repository */

package gender

import (
	"regexp"
)

var genderPattern = regexp.MustCompile(`^(Male|Female|Gay|Lesbian|Bisexual|Asexual|Other)$`)

// Gender : Validate a gender code.
func Gender(gender string) bool {
	return genderPattern.MatchString(gender)
}
