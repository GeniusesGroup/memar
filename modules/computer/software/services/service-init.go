/* For license and copyright information please see the LEGAL file in the code repository */

package captcha

import (
	"libgo/protocol"
)

func Init() {
	PhraseCaptchas.InitDefaults()

	protocol.App.RegisterService(&getNewPhraseCaptchaService)
	protocol.App.RegisterService(&getPhraseCaptchaAudioService)
	protocol.App.RegisterService(&solvePhraseCaptchaService)
}
