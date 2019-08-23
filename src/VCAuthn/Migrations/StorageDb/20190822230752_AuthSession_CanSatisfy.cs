using Microsoft.EntityFrameworkCore.Migrations;

namespace VCAuthn.Migrations
{
    public partial class AuthSession_CanSatisfy : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<bool>(
                name: "PresentationRequestSatisfied",
                table: "Sessions",
                nullable: false,
                defaultValue: false);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "PresentationRequestSatisfied",
                table: "Sessions");
        }
    }
}
