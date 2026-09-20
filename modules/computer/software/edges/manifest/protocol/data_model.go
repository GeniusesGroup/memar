/* For license and copyright information please see the LEGAL file in the code repository */

package ap_p

// ApplicationManifest introduce all data about an applications
type DataModel interface {
	Icon() []byte
	DomainName() string
	Email() string

	AppID() (appID uint16) // local OS application ID

	ContentPreferences()
	PresentationPreferences()
}
