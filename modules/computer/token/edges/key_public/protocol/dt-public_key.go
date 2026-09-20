/* For license and copyright information please see the LEGAL file in the code repository */

package public_key_p

type Field_PublicKey interface {
	PublicKey() PublicKey
}

// suggest use DER format
type PublicKey []byte
