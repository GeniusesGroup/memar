/* For license and copyright information please see the LEGAL file in the code repository */

package qu_p

type Field_URI interface {
	URI() URI
}

// Locale name in the Computer world.
// Value generate by `uri` protocols that indicate in `modules/uri` or other protocols from other repositories.
type URI []byte
