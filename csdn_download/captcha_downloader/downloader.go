package main

import (
	"crypto/md5"
	"crypto/rand"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"image/png"
	"io"
	"net/http"
	"os"
)

func getMd5String(s string) string {
	h := md5.New()
	h.Write([]byte(s))
	return hex.EncodeToString(h.Sum(nil))

}

func getGuid() string {
	b := make([]byte, 48)

	if _, err := io.ReadFull(rand.Reader, b); err != nil {
		return ""
	}
	return getMd5String(base64.URLEncoding.EncodeToString(b))
}

func main() {
	for i := 0; i < 50; i++ {
		resp, err := http.Get("http://download.csdn.net/index.php/rest/tools/validcode/source_ip_validate/10.5711163911089325")
		if err != nil {
			continue
		}
		fmt.Println(resp.ContentLength)
		filename := "./vcodes/" + getGuid() + ".png"
		file, err := os.Create(filename)
		if err != nil {
			continue
		}
		io.Copy(file, resp.Body)
		resp.Body.Close()
		captcha_file, _ := os.Open(filename)
		image, err := png.Decode(captcha_file)
		if err != nil {
			continue
		}
		fmt.Println("bounds", image.Bounds())
		//There are two kinds of captcha, we choose 48*20 pixel one.
		if (image.Bounds().Dx() != 48) && (image.Bounds().Dy() != 20) {
			os.Remove(filename)
			i--
		} else {
			fmt.Println("save ", filename)
		}

	}

}
