import axios from "axios";
export async function check() {
    try {
        const currentUrl = window.location.href;
        const urlSegments = currentUrl.split("/");
        const id = urlSegments[urlSegments.length - 1];
        let access_token = localStorage.getItem(`access_token-${id}`);
        if (access_token === null) {
            return false;
        }
        const tokenData = JSON.parse(atob(access_token.split('.')[1]));
        const expirationTimestamp = tokenData.exp * 1000;
        if (Date.now() >= expirationTimestamp - 2000) {
            throw new Error('token expired');
        }
        else {
            // console.log("outside")
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
            return true;
        }
    }
    catch (error) {
        try {
            let refreah = await refreshAccessToken()
            if (refreah == 'unsuccess') {
                return false}
            else {
                return true}}
        catch {
            console.error(error);
            if (alert('An error occurred while fetching the data.\nPlease login Again')) {
                this.$router.push('/login')
            }
        }
    }
}




async function refreshAccessToken() {

    try {
        // console.log("getting refresh token")
        const currentUrl = window.location.href;
        const urlSegments = currentUrl.split("/");
        const id = urlSegments[urlSegments.length - 1];

        let refresh_token = localStorage.getItem(`refresh_token-${id}`);

        const tokenData = JSON.parse(atob(refresh_token.split('.')[1]));
        // console.log(tokenData)
        const expirationTimestamp = tokenData.exp * 1000;
        // console.log(expirationTimestamp)

        if (Date.now() >= expirationTimestamp) {
            throw new Error('refresh token expired');
        }
        else {
            axios.defaults.headers.common["Authorization"] = "Bearer " + refresh_token;

            await axios.post("http://127.0.0.1:5000/api/token/refresh")
                .then((res) => {
                    let n_access_token = res.data.access_token;
                    // console.log(n_access_token)

                    localStorage.setItem(`access_token-${id}`, n_access_token);

                    axios.defaults.headers.common["Authorization"] = "Bearer " + n_access_token;
                    // console.log('sending true')

                    return 'true';

                })
                .catch((rej) => {
                    // console.log(rej)
                    alert("Please Login Againn")
                    return 'false';
                })
        }
    }

    catch {
        // alert("Please Login Again")
        // console.log("uncess starting")
        return "unsuccess"
    }


};


export default check;
