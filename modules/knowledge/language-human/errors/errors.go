/* For license and copyright information please see the LEGAL file in the code repository */

package lang

import (
	er "memar/error"
)

// Package errors
var (
	ErrBadLanguage er.Error
)

func init() {
	ErrBadLanguage.Init("domain/memar.scm.geniuses.group; package=language; type=error; name=bad-language")
}
