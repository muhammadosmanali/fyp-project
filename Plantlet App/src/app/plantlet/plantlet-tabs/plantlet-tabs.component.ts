import {Component, OnInit} from "@angular/core";
import {RouterExtensions} from "nativescript-angular/router";
import {ActivatedRoute} from "@angular/router";
import {Page} from "tns-core-modules/ui/page";
import {PlantletService} from "~/app/plantlet/plantlet.service";
import {AuthService} from "~/app/auth/auth.service";


@Component({
    selector: 'ns-plantlet-bars',
    templateUrl: './plantlet-tabs.component.html',
    styleUrls: ['./plantlet-tabs.component.scss'],
    moduleId: module.id,
})

export class PlantletTabsComponent implements OnInit{
    isLoading = false;

    constructor(private router: RouterExtensions,
                private plantletService: PlantletService,
                private active: ActivatedRoute,
                private page: Page,
                private authService: AuthService,) {}

    ngOnInit(): void {
        this.isLoading = true;
        this.plantletService.fetchPosts('all').subscribe();
        setTimeout(() => {
            this.plantletService.fetchCurrentUser().subscribe(
                res => {
                    this.isLoading = false;
                    this.loadTabRoutes();
                },
                err => {
                    console.log(err);
                    if(err.error["msg"] == "Token has expired") {
                        this.authService.logout();
                        console.log("log out");
                    }
                    this.loadTabRoutes();
                    this.isLoading = false;

                }
            );
        }, 4000);
        this.page.actionBarHidden = true;
    }

    private loadTabRoutes() {
        setTimeout(() => {
            this.router.navigate([
                {
                    outlets: {
                        home: ['home'],
                        community: ['community'],
                        you: ['you']
                    }
                }
            ],{
                relativeTo: this.active
            });
        }, 10);
    }

    onSelectedIndexChanged(args) {
        const tabView = args.object;
        const selectedTabViewItem = tabView.items[args.newIndex];
        switch (args.newIndex) {
            case 0:
                console.log("------------");
                console.log("home");
                break;
            case 1:
                console.log("------------");
                console.log("community");
                break;
            case 2:
                console.log("------------");

                console.log("you");
                break;
            default:
                break;
        }
    }

}
