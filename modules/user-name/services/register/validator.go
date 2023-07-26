/* For license and copyright information please see the LEGAL file in the code repository */

package validators

import "regexp"

var usernamePattern = regexp.MustCompile(`^[a-zA-](([\._\-][a-z0-9])|[a-z0-9]){0,62}$`)

// ValidateUsername use to validate a username string.
func ValidateUsername(username string) bool {
	return usernamePattern.MatchString(username)
}
