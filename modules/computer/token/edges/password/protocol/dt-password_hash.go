/* For license and copyright information please see the LEGAL file in the code repository */

package password_p

type Field_PasswordHash interface {
	PasswordHash() PasswordHash
}

type PasswordHash []byte
