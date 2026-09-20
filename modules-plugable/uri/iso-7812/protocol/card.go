/* For license and copyright information please see the LEGAL file in the code repository */

package card_p

// https://en.wikipedia.org/wiki/ISO/IEC_7812
type Card interface {
	// fixed size card number without any dash or space e.g. 1234123412341234
	Number() string

	// Major industry identifier
	MII() CardMII
	// Issuer identification number (IIN)
	IIN() string
	// Individual account identification
	Account() string
	// The final digit is a check digit which is calculated using the Luhn algorithm, defined in Annex B of ISO/IEC 7812-1.
	CheckDigit() byte
}

// Major Industry Identifier - the industry to which the card belongs to.
type CardMII byte

const (
	// 	ISO/TC 68 and other industry assignments : https://en.wikipedia.org/wiki/ISO/TC_68
	CardMII_ISO68 = '0'
	// 2	Airlines, financial and other future industry assignments
	CardMII_Airlines  = '1'
	CardMII_Airlines2 = '2'
	// Travel and entertainment
	CardMII_Travel = '3'
	// Banking and financial
	CardMII_Banking  = '4'
	CardMII_Banking2 = '5'
	// Merchandising and banking/financial
	CardMII_Merchandising = '6'
	// Petroleum and other future industry assignments
	CardMII_Petroleum = '7'
	// Healthcare, telecommunications and other future industry assignments
	CardMII_Telecommunications = '8'
	// For assignment by national standards bodies
	CardMII_National = '9'
)

func (mii CardMII) ToString() (industry string) {
	switch mii {
	case CardMII_ISO68:
		industry = "ISO/TC 68"
	case CardMII_Airlines, CardMII_Airlines2:
		industry = "Airlines"
	case CardMII_Travel:
		industry = "Travel and entertainment and banking/financial"
	case CardMII_Banking, CardMII_Banking2:
		industry = "Banking and financial"
	case CardMII_Merchandising:
		industry = "Merchandising and banking/financial"
	case CardMII_Petroleum:
		industry = "Petroleum"
	case CardMII_Telecommunications:
		industry = "Healthcare and telecommunications"
	case CardMII_National:
		industry = "National assignment"
	default:
		industry = "unknown"
	}
	return
}

// TODO::: detect card type??
// const (
// 	DebitCard
// 	CreditCard
// 	PrepaidCard
// )
