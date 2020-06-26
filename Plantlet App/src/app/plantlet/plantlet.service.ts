import {Injectable, OnInit} from "@angular/core";
import {AuthService} from "~/app/auth/auth.service";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {UrlService} from "~/app/shared/url.service";
import {switchMap, take, tap} from "rxjs/internal/operators";
import {BehaviorSubject, of, Subscription} from "rxjs";
import {PostModel} from "~/app/plantlet/community/post.model";

declare var android: any;

@Injectable({
    providedIn: 'root'
})
export class PlantletService implements OnInit{
    private _posts = new BehaviorSubject<PostModel>(null);

    authSub: Subscription;

    private accessToken: string;
    private user_id: string;

    constructor(private authService: AuthService,
                private http: HttpClient,
                private urlService: UrlService) {}


    ngOnInit(): void {
    }

    get posts() {
        return this._posts.asObservable();
    }

    /***
     *  ALL USER SERVICE FUNCTIONS
     *
     * ***/

    fetchCurrentUser() {
        return this.authService.user.pipe(
            take(1),
            switchMap(currentUser => {
                let headers = new HttpHeaders();
                headers = headers.set('Authorization', `Bearer ${currentUser.accessToken}`);
                if(!currentUser || !currentUser.isAuth) {
                    return of(null);
                }
                return this.http.get(
                    this.urlService.url + `/user/${currentUser.id}`,
                    {
                        headers: headers
                    }
                )
            })
        )
    }

    /***
     *  ALL COMMUNITY SERVICE FUNCTIONS
     *
     * ***/

    fetchPosts(which: string) {
        let url: string;
        return this.authService.user.pipe(
            take(1),
            switchMap(currentUser => {
                let headers = new HttpHeaders();
                headers = headers.set('Authorization', `Bearer ${currentUser.accessToken}`);
                if(!currentUser || !currentUser.isAuth) {
                    return of(null);
                }

                if(which === 'all') {
                    url = this.urlService.url + `/post/all`;
                } else if (which === 'list') {
                    url = this.urlService.url + `/post/list/${currentUser.id}`;
                } else {
                    return of(null);
                }

                return this.http.get<PostModel>(
                    url,
                    {headers: headers}
                ).pipe(
                    tap(resData => {
                        let loadedPost = new PostModel(resData.posts.sort((a, b) => Date.parse(b["post_date"]) - Date.parse(a["post_date"])));
                        this._posts.next(loadedPost);
                    })
                );
            })
        );
    }

    deletePost(id: number) {
        return this.authService.user.pipe(
            take(1),
            switchMap(currentUser => {
                let headers = new HttpHeaders();
                headers = headers.set('Authorization', `Bearer ${currentUser.accessToken}`);
                if(!currentUser || !currentUser.isAuth) {
                    return of(null);
                }
                return this.http.delete(
                    this.urlService.url + `/post/${id}`,
                    {
                        headers: headers
                    }
                )
            })
        )
    }
}

