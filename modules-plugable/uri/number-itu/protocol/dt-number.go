/* For license and copyright information please see the LEGAL file in the code repository */

package un_p

type Field_Number interface {
	Number() Number
}

// like PhoneNumber
// Number uint64          // without country code e.g. {(00)98-}912-345-6789
type Number string
