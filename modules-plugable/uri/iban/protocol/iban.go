/* For license and copyright information please see the LEGAL file in the code repository */

package faip

// IBAN or International Bank Account Number
// https://en.wikipedia.org/wiki/International_Bank_Account_Number
// https://github.com/persian-tools/go-persian-tools
type IBAN interface {
	IBAN() string

	CountryCode() string // country code using ISO 3166-1 alpha-2 – two letters
	CheckDigits() uint8  // two digits
	BBAN() string        // Basic Bank Account Number (BBAN) – up to 30 alphanumeric characters that are country-specific
}
